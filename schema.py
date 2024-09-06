from pydantic import BaseModel
from typing import List


class ReviewBase(BaseModel):
    content: str
    rating: int


class ReviewCreate(ReviewBase):
    pass


class Review(ReviewBase):
    id: int
    destination_id: int

    class Config:
        orm_mode = True


class DestinationBase(BaseModel):
    name: str
    description: str
    price: float


class DestinationCreate(DestinationBase):
    category_id: int


class Destination(DestinationBase):
    id: int
    category: List['Category'] = []
    reviews: List[Review] = []

    class Config:
        orm_mode = True


class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    id: int
    destinations: List[Destination] = []

    class Config:
        orm_mode = True
