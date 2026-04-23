from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Path, UserTopicProgress, User
from app.schemas import PathOut, TopicOut, PathOverviewOut, ExamQuestionOut
from app.auth import get_current_user

router = APIRouter(prefix="/paths", tags=["paths"])


@router.get("", response_model=list[PathOut])
def list_paths(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    paths = db.query(Path).all()
    result = []
    for path in paths:
        topic_ids = [t.id for t in path.topics]
        completed = db.query(UserTopicProgress).filter(
            UserTopicProgress.user_id == current_user.id,
            UserTopicProgress.topic_id.in_(topic_ids),
            UserTopicProgress.completed == True,
        ).count()
        result.append(PathOut(
            id=path.id, slug=path.slug, title=path.title,
            description=path.description, exam_slot=path.exam_slot,
            total_topics=len(topic_ids), completed_topics=completed,
        ))
    return result


@router.get("/{slug}/overview", response_model=PathOverviewOut)
def get_path_overview(slug: str, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    path = db.query(Path).filter(Path.slug == slug).first()
    if not path:
        raise HTTPException(status_code=404, detail="Path not found")
    return PathOverviewOut(
        overview=path.overview,
        exam_questions=[ExamQuestionOut.model_validate(q) for q in path.exam_questions],
    )


@router.get("/{slug}/topics", response_model=list[TopicOut])
def get_path_topics(slug: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    path = db.query(Path).filter(Path.slug == slug).first()
    if not path:
        raise HTTPException(status_code=404, detail="Path not found")
    result = []
    for topic in path.topics:
        progress = db.query(UserTopicProgress).filter(
            UserTopicProgress.user_id == current_user.id,
            UserTopicProgress.topic_id == topic.id,
        ).first()
        result.append(TopicOut(
            id=topic.id, slug=topic.slug, title=topic.title,
            description=topic.description, order=topic.order,
            completed=progress.completed if progress else False,
            depends_on=topic.depends_on or [],
        ))
    return result
