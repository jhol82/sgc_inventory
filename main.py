
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from database import Base, engine, get_db
from models import Item, Project
from schemas import (
    ItemCreate,
    ItemRead,
    ItemUpdate,
    ProjectCreate,
    ProjectRead,
    ProjectUpdate,
)

import models
import schemas
from database import Base, engine, get_db

# Create tables in the database (for now, instead of Alembic)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="SGC Inventory")


@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html>
        <head>
            <title>SGC Inventory</title>
        </head>
        <body style="font-family: Arial; padding: 20px;">
            <h1>SGC Inventory App</h1>
            <p>Inventory app is running.</p>
            <p>Database is connected and the 'items' table should now exist in your cloud Postgres.</p>
        </body>
    </html>
    """


# ---------- ITEM CRUD API ----------

@app.post("/items", response_model=schemas.ItemRead)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    """Create a new inventory item."""
    db_item = models.Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


from typing import Optional
from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from database import Base, engine, get_db
from models import Item
from schemas import ItemCreate, ItemRead, ItemUpdate

# (rest of your existing imports / code stay the same)

@app.get("/items", response_model=list[ItemRead])
def list_items(
    project: Optional[str] = Query(None, description="Filter by project name (contains)"),
    part_number: Optional[str] = Query(None, description="Filter by part number (contains)"),
    db: Session = Depends(get_db),
):
    """List items, optionally filtered by project and part number."""
    query = db.query(Item)

    if project:
        # case-insensitive contains match on project
        query = query.filter(Item.project.ilike(f"%{project}%"))

    if part_number:
        # case-insensitive contains match on part_number
        query = query.filter(Item.part_number.ilike(f"%{part_number}%"))

    items = query.order_by(Item.id.desc()).all()
    return items



@app.get("/items/{item_id}", response_model=schemas.ItemRead)
def get_item(item_id: int, db: Session = Depends(get_db)):
    """Get a single item by ID."""
    item = db.query(models.Item).get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.put("/items/{item_id}", response_model=schemas.ItemRead)
def update_item(item_id: int, item_update: schemas.ItemUpdate, db: Session = Depends(get_db)):
    """Update an item (part number, description, project, location, quantity)."""
    item = db.query(models.Item).get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    update_data = item_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(item, field, value)

    db.commit()
    db.refresh(item)
    return item
# ------------ PROJECT ROUTES ------------

@app.post("/projects", response_model=ProjectRead)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    db_project = Project(**project.dict())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


@app.get("/projects", response_model=list[ProjectRead])
def list_projects(db: Session = Depends(get_db)):
    projects = db.query(Project).order_by(Project.name.asc()).all()
    return projects


@app.get("/projects/{project_id}", response_model=ProjectRead)
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

