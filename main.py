from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional

from database import SessionLocal, engine
import models
import schema

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create Destination
@app.post("/destinations/", response_model=schema.Destination)
def create_destination(destination: schema.DestinationCreate, db: Session = Depends(get_db)):
    db_destination = models.Destination(
        name=destination.name,
        description=destination.description,
        price=destination.price,
        category_id=destination.category_id
    )
    db.add(db_destination)
    db.commit()
    db.refresh(db_destination)
    return db_destination


@app.get("/destinations/", response_model=List[schema.Destination])
def read_destinations(
        skip: int = 0,
        limit: int = 10,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        search: Optional[str] = None,
        category_id: Optional[int] = None,
        db: Session = Depends(get_db)
):
    query = db.query(models.Destination)

    if min_price:
        query = query.filter(models.Destination.price >= min_price)
    if max_price:
        query = query.filter(models.Destination.price <= max_price)
    if search:
        query = query.filter(models.Destination.name.contains(search))
    if category_id:
        query = query.filter(models.Destination.category_id == category_id)

    return query.offset(skip).limit(limit).all()


# Create Review
@app.post("/reviews/", response_model=schema.Review)
def create_review(review: schema.ReviewCreate, destination_id: int, db: Session = Depends(get_db)):
    db_review = models.Review(
        content=review.content,
        rating=review.rating,
        destination_id=destination_id
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


# Get Categories
@app.get("/categories/", response_model=List[schema.Category])
def read_categories(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(models.Category).offset(skip).limit(limit).all()


# Create Category
@app.post("/categories/", response_model=schema.Category)
def create_category(category: schema.CategoryCreate, db: Session = Depends(get_db)):
    db_category = models.Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category
