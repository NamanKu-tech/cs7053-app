from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, Boolean, Text, ForeignKey, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    progress: Mapped[list["UserTopicProgress"]] = relationship(back_populates="user")
    attempts: Mapped[list["MockAttempt"]] = relationship(back_populates="user")
    material_progress: Mapped[list["UserMaterialProgress"]] = relationship(back_populates="user")


class Path(Base):
    __tablename__ = "paths"
    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    exam_slot: Mapped[str] = mapped_column(String(10))
    overview: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    topics: Mapped[list["Topic"]] = relationship(back_populates="path", order_by="Topic.order")
    exam_questions: Mapped[list["ExamQuestion"]] = relationship(back_populates="path", order_by="ExamQuestion.year.desc()")


class Topic(Base):
    __tablename__ = "topics"
    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text, default="")
    path_id: Mapped[int] = mapped_column(ForeignKey("paths.id"))
    order: Mapped[int] = mapped_column(Integer)
    depends_on: Mapped[list] = mapped_column(JSON, default=list)
    path: Mapped["Path"] = relationship(back_populates="topics")
    notes: Mapped[list["Note"]] = relationship(back_populates="topic")
    progress: Mapped[list["UserTopicProgress"]] = relationship(back_populates="topic")
    materials: Mapped[list["TopicMaterial"]] = relationship(back_populates="topic", order_by="TopicMaterial.order")


class UserTopicProgress(Base):
    __tablename__ = "user_topic_progress"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    topic_id: Mapped[int] = mapped_column(ForeignKey("topics.id"))
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    user_note: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    note_public: Mapped[bool] = mapped_column(Boolean, default=False)
    user: Mapped["User"] = relationship(back_populates="progress")
    topic: Mapped["Topic"] = relationship(back_populates="progress")


class Note(Base):
    __tablename__ = "notes"
    id: Mapped[int] = mapped_column(primary_key=True)
    topic_id: Mapped[int] = mapped_column(ForeignKey("topics.id"))
    content: Mapped[str] = mapped_column(Text)
    is_prebuilt: Mapped[bool] = mapped_column(Boolean, default=False)
    topic: Mapped["Topic"] = relationship(back_populates="notes")


class Question(Base):
    __tablename__ = "questions"
    id: Mapped[int] = mapped_column(primary_key=True)
    topic_id: Mapped[int] = mapped_column(ForeignKey("topics.id"))
    year: Mapped[int] = mapped_column(Integer)
    exam_slot: Mapped[str] = mapped_column(String(10))
    question_text: Mapped[str] = mapped_column(Text)
    sample_answer: Mapped[str] = mapped_column(Text)
    marks: Mapped[int] = mapped_column(Integer)
    topic: Mapped["Topic"] = relationship(foreign_keys=[topic_id])


class ExamQuestion(Base):
    __tablename__ = "exam_questions"
    id: Mapped[int] = mapped_column(primary_key=True)
    path_id: Mapped[int] = mapped_column(ForeignKey("paths.id"))
    year: Mapped[int] = mapped_column(Integer)
    exam_slot: Mapped[str] = mapped_column(String(10))
    marks: Mapped[int] = mapped_column(Integer)
    question_text: Mapped[str] = mapped_column(Text)
    sample_answer: Mapped[str] = mapped_column(Text)
    path: Mapped["Path"] = relationship(back_populates="exam_questions")


class TopicMaterial(Base):
    __tablename__ = "topic_materials"
    id: Mapped[int] = mapped_column(primary_key=True)
    topic_id: Mapped[int] = mapped_column(ForeignKey("topics.id"))
    title: Mapped[str] = mapped_column(String(255))
    file: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    external_url: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    note: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    order: Mapped[int] = mapped_column(Integer, default=0)
    topic: Mapped["Topic"] = relationship(back_populates="materials")
    completions: Mapped[list["UserMaterialProgress"]] = relationship(back_populates="material")


class UserMaterialProgress(Base):
    __tablename__ = "user_material_progress"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    topic_material_id: Mapped[int] = mapped_column(ForeignKey("topic_materials.id"))
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    user: Mapped["User"] = relationship(back_populates="material_progress")
    material: Mapped["TopicMaterial"] = relationship(back_populates="completions")


class MockAttempt(Base):
    __tablename__ = "mock_attempts"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    question_id: Mapped[int] = mapped_column(Integer)
    answer_text: Mapped[str] = mapped_column(Text)
    score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    feedback: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="pending")
    attempted_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    user: Mapped["User"] = relationship(back_populates="attempts")

