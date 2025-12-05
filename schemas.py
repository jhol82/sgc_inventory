from datetime import datetime
from typing import Optional

from pydantic import BaseModel
# ------------ PROJECT SCHEMAS ------------

class ProjectBase(BaseModel):
    name: str
    code: Optional[str] = None
    client: Optional[str] = None
    city: Optional[str] = None
    notes: Optional[str] = None
    active: bool = True


class ProjectCreate(ProjectBase):
    """Fields required when creating a project (same as base for now)."""
    pass


class ProjectUpdate(BaseModel):
    """Fields allowed when updating a project."""
    name: Optional[str] = None
    code: Optional[str] = None
    client: Optional[str] = None
    city: Optional[str] = None
    notes: Optional[str] = None
    active: Optional[bool] = None


class ProjectRead(ProjectBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class ItemBase(BaseModel):
    part_number: str
    description: Optional[str] = None
    project: Optional[str] = None
    location: Optional[str] = None
    quantity: int


class ItemCreate(ItemBase):
    """Fields required when creating an item."""
    pass


class ItemUpdate(BaseModel):
    """Fields you can change when updating an item."""
    part_number: Optional[str] = None
    description: Optional[str] = None
    project: Optional[str] = None
    location: Optional[str] = None
    quantity: Optional[int] = None


class ItemRead(ItemBase):
    """What we return to the client."""
    id: int

    class Config:
        orm_mode = True  # lets FastAPI read SQLAlchemy objects
