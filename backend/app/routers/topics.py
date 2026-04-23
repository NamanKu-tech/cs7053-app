from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Topic, Note, Question, UserTopicProgress, User, TopicMaterial, UserMaterialProgress
from app.schemas import NoteOut, QuestionOut, UserNoteRequest, ProgressToggleRequest, TopicMaterialOut, TopicMaterialsResponse
from app.auth import get_current_user

router = APIRouter(prefix="/topics", tags=["topics"])


def _get_topic_or_404(slug: str, db: Session) -> Topic:
    topic = db.query(Topic).filter(Topic.slug == slug).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic


def _get_or_create_progress(user_id: int, topic_id: int, db: Session) -> UserTopicProgress:
    progress = db.query(UserTopicProgress).filter(
        UserTopicProgress.user_id == user_id,
        UserTopicProgress.topic_id == topic_id,
    ).first()
    if not progress:
        progress = UserTopicProgress(user_id=user_id, topic_id=topic_id)
        db.add(progress)
    return progress


@router.get("/{slug}/notes/prebuilt", response_model=NoteOut)
def get_prebuilt_note(slug: str, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    topic = _get_topic_or_404(slug, db)
    note = db.query(Note).filter(Note.topic_id == topic.id, Note.is_prebuilt == True).first()
    if not note:
        return NoteOut(content="No notes yet for this topic.", is_prebuilt=True)
    return NoteOut(content=note.content, is_prebuilt=True)


@router.get("/{slug}/notes/user", response_model=NoteOut)
def get_user_note(slug: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    topic = _get_topic_or_404(slug, db)
    progress = db.query(UserTopicProgress).filter(
        UserTopicProgress.user_id == current_user.id,
        UserTopicProgress.topic_id == topic.id,
    ).first()
    content = progress.user_note if progress and progress.user_note else ""
    return NoteOut(content=content, is_prebuilt=False)


@router.patch("/{slug}/notes/user")
def save_user_note(slug: str, body: UserNoteRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    topic = _get_topic_or_404(slug, db)
    progress = _get_or_create_progress(current_user.id, topic.id, db)
    progress.user_note = body.content
    db.commit()
    return {"saved": True}


@router.get("/{slug}/questions", response_model=list[QuestionOut])
def get_questions(slug: str, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    topic = _get_topic_or_404(slug, db)
    return db.query(Question).filter(Question.topic_id == topic.id).order_by(Question.year.desc()).all()


@router.get("/{slug}/progress")
def get_progress(slug: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    topic = _get_topic_or_404(slug, db)
    progress = db.query(UserTopicProgress).filter(
        UserTopicProgress.user_id == current_user.id,
        UserTopicProgress.topic_id == topic.id,
    ).first()
    return {"completed": progress.completed if progress else False}


@router.post("/{slug}/progress")
def toggle_progress(slug: str, body: ProgressToggleRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    topic = _get_topic_or_404(slug, db)
    progress = _get_or_create_progress(current_user.id, topic.id, db)
    progress.completed = body.completed
    progress.completed_at = datetime.utcnow() if body.completed else None
    db.commit()
    return {"completed": progress.completed}


@router.get("/{slug}/materials", response_model=TopicMaterialsResponse)
def get_materials(slug: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    topic = _get_topic_or_404(slug, db)
    materials = db.query(TopicMaterial).filter(TopicMaterial.topic_id == topic.id).order_by(TopicMaterial.order).all()
    completed_ids = {
        row.topic_material_id
        for row in db.query(UserMaterialProgress).filter(
            UserMaterialProgress.user_id == current_user.id,
            UserMaterialProgress.topic_material_id.in_([m.id for m in materials]),
            UserMaterialProgress.completed == True,
        ).all()
    }
    out = [
        TopicMaterialOut(
            id=m.id, title=m.title, file=m.file, external_url=m.external_url,
            note=m.note, order=m.order, completed=m.id in completed_ids,
        )
        for m in materials
    ]
    progress = round(len(completed_ids) / len(materials) * 100) if materials else 0
    return TopicMaterialsResponse(materials=out, progress=progress)


@router.post("/{slug}/materials/{material_id}/toggle")
def toggle_material(slug: str, material_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    topic = _get_topic_or_404(slug, db)
    material = db.query(TopicMaterial).filter(TopicMaterial.id == material_id, TopicMaterial.topic_id == topic.id).first()
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    row = db.query(UserMaterialProgress).filter(
        UserMaterialProgress.user_id == current_user.id,
        UserMaterialProgress.topic_material_id == material_id,
    ).first()
    if not row:
        row = UserMaterialProgress(user_id=current_user.id, topic_material_id=material_id, completed=True, completed_at=datetime.utcnow())
        db.add(row)
    else:
        row.completed = not row.completed
        row.completed_at = datetime.utcnow() if row.completed else None
    db.commit()
    return {"completed": row.completed}
