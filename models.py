from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    destinations = relationship("Destination", back_populates="category")


class Destination(Base):
    __tablename__ = "destinations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text, index=True)
    price = Column(Float, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"))

    category = relationship("Category", back_populates="destinations")
    reviews = relationship("Review", back_populates="destination")


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, index=True)
    rating = Column(Integer)
    destination_id = Column(Integer, ForeignKey("destinations.id"))

    destination = relationship("Destination", back_populates="reviews")
