from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from db.database import Base
import enum

class SourceEnum(str, enum.Enum):
    MEETING = "meeting"
    JOURNAL = "journal"
    CLIP = "clip"

class Meeting(Base):
    __tablename__ = "meetings"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    date = Column(DateTime)
    participants = Column(String)
    summary = Column(String)

    actions = relationship("ActionItem", back_populates="meeting")
    decisions = relationship("Decision", back_populates="meeting")
    blockers = relationship("Blocker", back_populates="meeting")

class Journal(Base):
    __tablename__ = "journals"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    summary = Column(String)
    date = Column(DateTime)
    theme = Column(String)        # could be JSON/array later
    strength = Column(String)     # could be JSON/array later
    growth_area = Column(String)  # could be JSON/array later

class Clip(Base):
    __tablename__ = "clips"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    summary = Column(String)
    date = Column(DateTime)

class ActionItem(Base):
    __tablename__ = "action_items"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    date = Column(DateTime)
    due_date = Column(DateTime)
    status = Column(String, default="open")
    personal = Column(Boolean, default=False)

    source = Column(Enum(SourceEnum))
    source_id = Column(Integer)
    meeting_id = Column(Integer, ForeignKey("meetings.id"))

    meeting = relationship("Meeting", back_populates="actions")

class Decision(Base):
    __tablename__ = "decisions"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    date = Column(DateTime)
    other_options = Column(String)  # JSON/array later
    personal = Column(Boolean, default=False)

    source = Column(Enum(SourceEnum))
    source_id = Column(Integer)
    meeting_id = Column(Integer, ForeignKey("meetings.id"))

    meeting = relationship("Meeting", back_populates="decisions")

class Blocker(Base):
    __tablename__ = "blockers"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    date = Column(DateTime)
    personal = Column(Boolean, default=False)

    source = Column(Enum(SourceEnum))
    source_id = Column(Integer)
    meeting_id = Column(Integer, ForeignKey("meetings.id"))

    meeting = relationship("Meeting", back_populates="blockers")