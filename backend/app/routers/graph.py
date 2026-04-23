from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Topic, Path, UserTopicProgress, User
from app.auth import get_current_user

router = APIRouter(prefix="/graph", tags=["graph"])

_PATH_COLORS = {"Q1": "#f59e0b", "Q2": "#3b82f6", "Q3": "#10b981", "Q4": "#8b5cf6"}
_PATH_COLS = {"Q1": 0, "Q2": 1, "Q3": 2, "Q4": 3}


@router.get("")
def get_graph(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    completed_topic_ids = {
        p.topic_id for p in db.query(UserTopicProgress).filter(
            UserTopicProgress.user_id == current_user.id,
            UserTopicProgress.completed == True,
        ).all()
    }

    nodes = []
    edges = []
    path_row_counter: dict[str, int] = {}

    for topic in db.query(Topic).join(Path).order_by(Path.id, Topic.order).all():
        exam_slot = topic.path.exam_slot
        col = _PATH_COLS.get(exam_slot, 0)
        row = path_row_counter.get(exam_slot, 0)
        path_row_counter[exam_slot] = row + 1

        is_done = topic.id in completed_topic_ids
        color = "#16a34a" if is_done else _PATH_COLORS.get(exam_slot, "#6b7280")

        nodes.append({
            "id": topic.slug,
            "data": {"label": topic.title, "status": "completed" if is_done else "not_started", "exam_slot": exam_slot},
            "position": {"x": col * 280, "y": row * 100},
            "style": {"background": color, "color": "#fff", "border": "none", "borderRadius": "8px", "padding": "8px 12px", "fontSize": "12px", "width": 200},
        })

        for dep_slug in (topic.depends_on or []):
            edges.append({"id": f"{dep_slug}->{topic.slug}", "source": dep_slug, "target": topic.slug, "style": {"stroke": "#94a3b8"}})

    return {"nodes": nodes, "edges": edges}
