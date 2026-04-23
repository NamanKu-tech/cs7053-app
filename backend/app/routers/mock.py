import os
import json
import httpx
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.database import get_db
from app.models import MockAttempt, ExamQuestion, Path, User
from app.schemas import GradeRequest, AttemptOut, ExamCardOut, ExamGroupOut, ExamPartOut, ExamGradeRequest, ExamGradeResponse, ExamGradeItemResult
from app.auth import get_current_user

router = APIRouter(prefix="/mock", tags=["mock"])

# Each card: 4 groups (Q1–Q4), each group = one year's a/b/c parts for that path
_EXAM_CARDS = [
    {"id": 1,  "title": "Mock Exam 1",  "difficulty": "easy",   "groups": [
        ("Q1", "q1-risk-analysis", 2025), ("Q2", "q2-tls-protocols", 2025),
        ("Q3", "q3-system-design", 2025), ("Q4", "q4-dns-dnssec", 2025),
    ]},
    {"id": 2,  "title": "Mock Exam 2",  "difficulty": "easy",   "groups": [
        ("Q1", "q1-risk-analysis", 2024), ("Q2", "q2-tls-protocols", 2024),
        ("Q3", "q3-system-design", 2024), ("Q4", "q4-dns-dnssec", 2024),
    ]},
    {"id": 3,  "title": "Mock Exam 3",  "difficulty": "easy",   "groups": [
        ("Q1", "q1-risk-analysis", 2023), ("Q2", "q2-tls-protocols", 2023),
        ("Q3", "q3-system-design", 2023), ("Q4", "q4-dns-dnssec", 2023),
    ]},
    {"id": 4,  "title": "Mock Exam 4",  "difficulty": "medium", "groups": [
        ("Q1", "q1-risk-analysis", 2025), ("Q2", "q2-tls-protocols", 2022),
        ("Q3", "q3-system-design", 2023), ("Q4", "q4-dns-dnssec", 2024),
    ]},
    {"id": 5,  "title": "Mock Exam 5",  "difficulty": "medium", "groups": [
        ("Q1", "q1-risk-analysis", 2024), ("Q2", "q2-tls-protocols", 2025),
        ("Q3", "q3-system-design", 2022), ("Q4", "q4-dns-dnssec", 2023),
    ]},
    {"id": 6,  "title": "Mock Exam 6",  "difficulty": "medium", "groups": [
        ("Q1", "q1-risk-analysis", 2022), ("Q2", "q2-tls-protocols", 2020),
        ("Q3", "q3-system-design", 2024), ("Q4", "q4-dns-dnssec", 2022),
    ]},
    {"id": 7,  "title": "Mock Exam 7",  "difficulty": "medium", "groups": [
        ("Q1", "q1-risk-analysis", 2023), ("Q2", "q2-tls-protocols", 2024),
        ("Q3", "q3-system-design", 2020), ("Q4", "q4-dns-dnssec", 2025),
    ]},
    {"id": 8,  "title": "Mock Exam 8",  "difficulty": "hard",   "groups": [
        ("Q1", "q1-risk-analysis", 2020), ("Q2", "q2-tls-protocols", 2019),
        ("Q3", "q3-system-design", 2020), ("Q4", "q4-dns-dnssec", 2019),
    ]},
    {"id": 9,  "title": "Mock Exam 9",  "difficulty": "hard",   "groups": [
        ("Q1", "q1-risk-analysis", 2019), ("Q2", "q2-tls-protocols", 2020),
        ("Q3", "q3-system-design", 2019), ("Q4", "q4-dns-dnssec", 2020),
    ]},
    {"id": 10, "title": "Mock Exam 10", "difficulty": "hard",   "groups": [
        ("Q1", "q1-risk-analysis", 2018), ("Q2", "q2-tls-protocols", 2017),
        ("Q3", "q3-system-design", 2016), ("Q4", "q4-dns-dnssec", 2018),
    ]},
]

_GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-pro-preview:generateContent"

_GRADING_PROMPT = (
    "You are an exam grader for a graduate-level Security & Privacy course at Trinity College Dublin (CS7053).\n\n"
    "You are given a GRADING GUIDE written by the examiner. "
    "Use it to understand what concepts, structure, and depth are expected — but do NOT treat it as a model answer to match verbatim. "
    "A student who demonstrates the same understanding through different wording, examples, or structure should be awarded full marks. "
    "Reward conceptual correctness, technical accuracy, and appropriate depth. "
    "Penalise vague, incomplete, or generic answers that miss key concepts from the grading guide.\n\n"
    "Your feedback must:\n"
    "1. State what the student did well (specific concepts or points they got right)\n"
    "2. Identify exactly which key concepts from the grading guide were missing or underdeveloped\n"
    "3. Explain why those gaps cost marks\n"
    "4. Give concrete, actionable suggestions for how the student can improve on their next attempt — "
    "name the specific topics, techniques, or depth of explanation they should add\n\n"
    'Return JSON only with no markdown fences: {{"score": <integer 0-10>, "feedback": "<detailed feedback covering all 4 points above, 6-10 sentences>"}}\n\n'
    "QUESTION ({marks} marks):\n{question}\n\n"
    "EXAMINER GRADING GUIDE (use for criteria, not as a model answer):\n{sample}\n\n"
    "STUDENT ANSWER:\n{student}"
)


def _call_gemini(prompt: str) -> tuple[int | None, str]:
    api_key = os.getenv("GEMINI_API_KEY", "")
    if not api_key:
        return None, "Grading service unavailable. Try again."
    try:
        response = httpx.post(
            _GEMINI_URL,
            params={"key": api_key},
            json={"contents": [{"parts": [{"text": prompt}]}]},
            timeout=30,
        )
        response.raise_for_status()
        text = response.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
        data = json.loads(text)
        return int(data["score"]), str(data["feedback"])
    except Exception:
        return None, "Grading service unavailable. Try again."


@router.get("/exams", response_model=list[ExamCardOut])
def get_exam_cards(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    path_id_map = {p.slug: p.id for p in db.query(Path).all()}
    result = []
    for card in _EXAM_CARDS:
        groups = []
        for (slot, path_slug, year) in card["groups"]:
            path_id = path_id_map.get(path_slug)
            if not path_id:
                continue
            parts_rows = (
                db.query(ExamQuestion)
                .filter(ExamQuestion.path_id == path_id, ExamQuestion.year == year)
                .order_by(ExamQuestion.exam_slot)
                .all()
            )
            parts = [ExamPartOut(id=p.id, exam_slot=p.exam_slot, marks=p.marks, question_text=p.question_text) for p in parts_rows]
            groups.append(ExamGroupOut(slot=slot, year=year, parts=parts))
        result.append(ExamCardOut(id=card["id"], title=card["title"], difficulty=card["difficulty"], groups=groups))
    return result


@router.post("/grade-exam", response_model=ExamGradeResponse)
def grade_exam(body: ExamGradeRequest, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    results = []
    for item in body.items:
        eq = db.get(ExamQuestion, item.exam_question_id)
        if not eq:
            results.append(ExamGradeItemResult(exam_question_id=item.exam_question_id, score=None, feedback="Question not found."))
            continue
        prompt = _GRADING_PROMPT.format(
            marks=eq.marks,
            question=eq.question_text,
            sample=eq.sample_answer,
            student=item.answer_text or "(no answer provided)",
        )
        score, feedback = _call_gemini(prompt)
        results.append(ExamGradeItemResult(exam_question_id=item.exam_question_id, score=score, feedback=feedback))
    return ExamGradeResponse(results=results)


def _grade_in_background(attempt_id: int, prompt: str):
    db = SessionLocal()
    try:
        attempt = db.get(MockAttempt, attempt_id)
        if not attempt:
            return
        score, feedback = _call_gemini(prompt)
        attempt.score = score
        attempt.feedback = feedback
        attempt.status = "complete"
        db.commit()
    finally:
        db.close()


@router.post("/grade")
def grade_answer(body: GradeRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    question = db.get(ExamQuestion, body.question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    attempt = MockAttempt(
        user_id=current_user.id,
        question_id=body.question_id,
        answer_text=body.answer_text,
        status="pending",
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    prompt = _GRADING_PROMPT.format(
        marks=question.marks,
        question=question.question_text,
        sample=question.sample_answer,
        student=body.answer_text,
    )
    background_tasks.add_task(_grade_in_background, attempt.id, prompt)
    return {"attempt_id": attempt.id, "status": "pending"}


@router.get("/attempts/{attempt_id}")
def get_attempt(attempt_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    attempt = db.get(MockAttempt, attempt_id)
    if not attempt or attempt.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Attempt not found")
    return {"attempt_id": attempt.id, "status": attempt.status, "score": attempt.score, "feedback": attempt.feedback}


@router.get("/history/{question_id}", response_model=list[AttemptOut])
def get_history(question_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return (
        db.query(MockAttempt)
        .filter(MockAttempt.user_id == current_user.id, MockAttempt.question_id == question_id)
        .order_by(MockAttempt.attempted_at.desc())
        .all()
    )
