from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from db.database import Base
import enum
from typing import Optional
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Enum, ARRAY, JSON

class SourceEnum(str, enum.Enum):
    MEETING = "meeting"
    JOURNAL = "journal"
    CLIP = "clip"

class ActionItemStatus(str, enum.Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    IGNORED = "ignored"

class BlockerStatus(str, enum.Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    ESCALATED = "escalated"
    IGNORED = "ignored"

class DecisionStatus(str, enum.Enum):
    OPEN = "open"
    DECIDED = "decided"
    IMPLEMENTED = "implemented"
    CANCELLED = "cancelled"

class Meeting(Base):
    __tablename__ = "meeting"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    date = Column(DateTime)
    participants = Column(JSON)  # Changed to JSON to store lists
    summary = Column(String)

    action_items = relationship("Action_Item", back_populates="meeting")
    decisions = relationship("Decision", back_populates="meeting")
    blockers = relationship("Blocker", back_populates="meeting")

class Journal(Base):
    __tablename__ = "journal"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    summary = Column(String)
    date = Column(DateTime)
    theme = Column(String)        # could be JSON/array later
    strength = Column(String)     # could be JSON/array later
    growth_area = Column(String)  # could be JSON/array later

class Clip(Base):
    __tablename__ = "clip"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    summary = Column(String)
    date = Column(DateTime)

class Action_Item(Base):
    __tablename__ = "action_item"

    id = Column(Integer, primary_key=True, index=True)
    meeting_id = Column(Integer, ForeignKey("meeting.id"), nullable=True)
    description = Column(String)
    due_date = Column(DateTime, nullable=True)
    status = Column(Enum(ActionItemStatus), default=ActionItemStatus.OPEN)
    
    personal = Column(Boolean, default=False)
    source: Optional[str] = Column(String, nullable=True)
    source_id: Optional[int] = Column(Integer, nullable=True)

    meeting = relationship("Meeting", back_populates="action_items")

class Decision(Base):
    __tablename__ = "decision"

    id = Column(Integer, primary_key=True, index=True)
    meeting_id = Column(Integer, ForeignKey("meeting.id"), nullable=True)
    description = Column(String)
    other_options = Column(JSON, nullable=True)
    status = Column(Enum(DecisionStatus), default=DecisionStatus.OPEN)
    personal = Column(Boolean, default=False)
    source = Column(String, nullable=True)
    source_id = Column(Integer, nullable=True)

    meeting = relationship("Meeting", back_populates="decisions")

class Blocker(Base):
    __tablename__ = "blocker"

    id = Column(Integer, primary_key=True, index=True)
    meeting_id = Column(Integer, ForeignKey("meeting.id"), nullable=True)
    description = Column(String)
    status = Column(Enum(BlockerStatus), default=BlockerStatus.OPEN)
    personal = Column(Boolean, default=False)
    source = Column(String, nullable=True)
    source_id = Column(Integer, nullable=True)

    meeting = relationship("Meeting", back_populates="blockers")