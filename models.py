from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.sql import func
from database import Base
class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    # Example: "Ismaili Center Houston"
    name = Column(String, unique=True, index=True, nullable=False)

    # Example: internal job number or short code like "ICH-HOU-01"
    code = Column(String, unique=True, index=True, nullable=True)

    # Example: "McCarthy", "Manhattan", etc.
    client = Column(String, nullable=True)

    # City / location if you want it
    city = Column(String, nullable=True)

    # Freeform notes
    notes = Column(Text, nullable=True)

    # Mark active/inactive instead of deleting
    active = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())



class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    part_number = Column(String(100), index=True, nullable=False)
    description = Column(String(255), nullable=True)
    project = Column(String(100), nullable=True)
    location = Column(String(100), nullable=True)
    quantity = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

