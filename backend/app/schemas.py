from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class PathOut(BaseModel):
    id: int
    slug: str
    title: str
    description: str
    exam_slot: str
    total_topics: int
    completed_topics: int
    model_config = {"from_attributes": True}


class TopicOut(BaseModel):
    id: int
    slug: str
    title: str
    description: str
    order: int
    completed: bool
    depends_on: list[str]
    model_config = {"from_attributes": True}


class NoteOut(BaseModel):
    content: str
    is_prebuilt: bool


class QuestionOut(BaseModel):
    id: int
    year: int
    exam_slot: str
    marks: int
    question_text: str
    sample_answer: str
    model_config = {"from_attributes": True}


class ProgressToggleRequest(BaseModel):
    completed: bool


class UserNoteRequest(BaseModel):
    content: str
    is_public: bool = False


class CommunityNoteOut(BaseModel):
    author: str
    content: str


class GradeRequest(BaseModel):
    question_id: int
    answer_text: str


class GradeResponse(BaseModel):
    score: Optional[int]
    feedback: str


class AttemptOut(BaseModel):
    id: int
    score: Optional[int]
    feedback: Optional[str]
    answer_text: str
    attempted_at: datetime
    model_config = {"from_attributes": True}


class ExamQuestionOut(BaseModel):
    id: int
    year: int
    exam_slot: str
    marks: int
    question_text: str
    sample_answer: str
    model_config = {"from_attributes": True}


class PathOverviewOut(BaseModel):
    overview: Optional[str]
    exam_questions: list[ExamQuestionOut]


class TopicMaterialOut(BaseModel):
    id: int
    title: str
    file: Optional[str]
    external_url: Optional[str]
    note: Optional[str]
    order: int
    completed: bool
    model_config = {"from_attributes": True}


class TopicMaterialsResponse(BaseModel):
    materials: list[TopicMaterialOut]
    progress: int  # 0-100


class ExamPartOut(BaseModel):
    id: int
    exam_slot: str
    marks: int
    question_text: str
    model_config = {"from_attributes": True}


class ExamGroupOut(BaseModel):
    slot: str   # "Q1" | "Q2" | "Q3" | "Q4"
    year: int
    parts: list[ExamPartOut]


class ExamCardOut(BaseModel):
    id: int
    title: str
    difficulty: str  # "easy" | "medium" | "hard"
    groups: list[ExamGroupOut]


class ExamGradeItem(BaseModel):
    exam_question_id: int
    answer_text: str


class ExamGradeRequest(BaseModel):
    items: list[ExamGradeItem]


class ExamGradeItemResult(BaseModel):
    exam_question_id: int
    score: Optional[int]
    feedback: str


class ExamGradeResponse(BaseModel):
    results: list[ExamGradeItemResult]
