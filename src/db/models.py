from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from db.database import Base
import enum
from typing import Optional
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Enum, ARRAY
class SourceEnum(str, enum.Enum):
    MEETING = "meeting"
    JOURNAL = "journal"
    CLIP = "clip"

class Meeting(Base):
    __tablename__ = "meeting"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    date = Column(DateTime)
    participants = Column(String)
    summary = Column(String)

    actions = relationship("ActionItem", back_populates="meeting")
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
    personal = Column(Boolean, default=False)
    source = Column(String, nullable=True)
    source_id = Column(Integer, nullable=True)

    meeting = relationship("Meeting", back_populates="decisions")

class Blocker(Base):
    __tablename__ = "blocker"

    id = Column(Integer, primary_key=True, index=True)
    meeting_id = Column(Integer, ForeignKey("meeting.id"), nullable=True)
    description = Column(String)
    personal = Column(Boolean, default=False)
    source = Column(String, nullable=True)
    source_id = Column(Integer, nullable=True)

    meeting = relationship("Meeting", back_populates="blockers")