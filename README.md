# Fast_API8
FastAPI Tutorial 8 dars
#  Filters, Search, va Query Parameters

Bu darsda, FastAPI da query parametrlari orqali filtering, full-text search, va ORM orqali kompleks querylarni yaratish usullarini ko'rib chiqamiz. Ushbu mavzular har qanday murakkab backend tizimlarda ma'lumotlarni qidirish va saralash imkoniyatini beruvchi asosiy vositalardan biridir.

### Query Parameters orqali Filtering
Query parametrlar HTTP so'rovlarida URL orqali yuboriladigan parametrlar hisoblanadi. FastAPI da query parametrlar yordamida ma'lumotlarni filtrlay olishimiz mumkin. Misol uchun, foydalanuvchidan ma'lum bir mezonlar asosida ma'lumotlarni so'rash mumkin (masalan, narx, kategoriya, va hokazo).

### Full-Text Search
Full-text search foydalanuvchilarga matn ichida so'zni yoki frazani qidirish imkonini beradi. SQLAlchemy yordamida qidiruvni amalga oshirish mumkin, lekin katta loyihalarda Elasticsearch kabi maxsus qidiruv motorlaridan foydalanish tavsiya etiladi.

### ORM orqali Kompleks Querylar Yaratish
ORM (Object-Relational Mapping) orqali ma'lumotlar bazasi jadvallarida murakkab querylarni yozish mumkin. Misol uchun, JOIN, GROUP BY, va ORDER BY kabi SQL buyruqlarini ORM yordamida ifodalash mumkin.


# Filters, Search, va Query Parameters haqida tushuncha
Filters, Search, va Query Parameters - bular backend tizimlarda foydalanuvchilarga kerakli ma'lumotlarni topish, qidirish va filtrlay olish imkoniyatini beruvchi asosiy vositalar hisoblanadi. Bu vositalar yordamida ma'lumotlar bazasidan ma'lumotlarni kerakli kriteriyalar asosida olish, saralash va ko'rsatish mumkin.

1. Query Parameters - HTTP so'rovlarida URL orqali yuboriladigan parametrlar. Ular URL oxirida ?key=value formatida qo'shiladi va server tomonida ma'lumotlarni saralash va filtrlash uchun ishlatiladi.

2. Filters - Filtrlar yordamida ma'lumotlarni aniq bir kriteriyalar bo'yicha ajratib olish mumkin. Misol uchun, narxi ma'lum bir qiymatdan yuqori yoki past bo'lgan mahsulotlarni ko'rsatish.

3. Search - Ma'lumotlar ichida matn bo'yicha qidirish imkoniyati. Masalan, mahsulot nomi yoki tavsifi bo'yicha qidirish.

### FastAPI da Filters, Search, va Query Parametersdan foydalanish
Keling, ushbu tushunchalarni kodlar orqali ko'rib chiqamiz:

1. Query Parameters
Query parametrlar orqali oddiy saralashni amalga oshirish uchun FastAPI da kerakli parametrlarni endpoint funksiyasiga qo'shamiz. Parametrlar ixtiyoriy bo'lsa, ular Optional qilib belgilanishi kerak.

Misol: Oddiy mahsulotlarni olish API
```python
from fastapi import FastAPI
from typing import Optional, List

app = FastAPI()

products = [
    {"id": 1, "name": "Laptop", "price": 1000},
    {"id": 2, "name": "Smartphone", "price": 500},
    {"id": 3, "name": "Tablet", "price": 300},
]

@app.get("/products/")
def read_products(skip: int = 0, limit: int = 10):
    return products[skip: skip + limit]

```
### Tushuntirish:

* skip va limit query parametrlar bo'lib, ular ma'lumotlarni nechta o‘tkazish va necha dona ko‘rsatishni belgilaydi.
* skip - ma'lumotlar ro'yxatidan qancha elementni tashlab o'tish kerakligini bildiradi.
* limit - ro'yxatdagi necha dona elementni ko'rsatish kerakligini bildiradi.

* URL misol: http://localhost:8000/products/?skip=0&limit=2

2. Filtering
Filtrlarni qo'llashda, ma'lumotlar ro'yxati kerakli kriteriyalarga mos keladigan bo'lishi kerak.

Misol: Narx bo'yicha filterlash
```python
@app.get("/products/filter/")
def filter_products(min_price: Optional[float] = None, max_price: Optional[float] = None):
    filtered_products = products
    if min_price is not None:
        filtered_products = [p for p in filtered_products if p["price"] >= min_price]
    if max_price is not None:
        filtered_products = [p for p in filtered_products if p["price"] <= max_price]
    return filtered_products
```

### Tushuntirish:

min_price va max_price parametrlari foydalanuvchi tomonidan ko'rsatilgan narx oralig'iga mos keluvchi mahsulotlarni tanlashda ishlatiladi.
if min_price is not None: - agar min_price ko'rsatilgan bo'lsa, filter shartini qo'llaydi.
URL misol: http://localhost:8000/products/filter/?min_price=300&max_price=800

3. Full-Text Search
Full-text search ma'lumotlar ichida matn bo'yicha qidiruvni amalga oshiradi. SQLAlchemy ORM va SQLite yoki boshqa DBMS yordamida matnli qidiruvni amalga oshirish mumkin.

Misol: Mahsulot nomi bo'yicha qidiruv
```python
@app.get("/products/search/")
def search_products(search: Optional[str] = None):
    if search:
        return [p for p in products if search.lower() in p["name"].lower()]
    return products

```
### Tushuntirish:

* search parametri foydalanuvchidan qidiriladigan matnni oladi.
* if search: - agar qidiruv matni berilgan bo'lsa, mahsulotlar nomida ushbu matn mavjudligini tekshiradi.
* .lower() yordamida katta va kichik harflarni hisobga olmaslik uchun qidiruv matnini kichik harfga o'tkazamiz.

* URL misol: http://localhost:8000/products/search/?search=laptop

4. ORM orqali murakkab querylar yaratish
SQLAlchemy ORM yordamida, FastAPI da murakkab querylarni yaratish mumkin. Keling, ma'lumotlar bazasida filtrlar va qidiruvni qanday amalga oshirishni ko'rib chiqamiz.

Misol: SQLAlchemy yordamida filtering va qidiruv

```python
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/products/")
def read_products(skip: int = 0, limit: int = 10, min_price: Optional[float] = None, max_price: Optional[float] = None, search: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(models.Product)
    
    if min_price:
        query = query.filter(models.Product.price >= min_price)
    if max_price:
        query = query.filter(models.Product.price <= max_price)
    if search:
        query = query.filter(models.Product.name.contains(search))
    
    return query.offset(skip).limit(limit).all()
```
### Tushuntirish:

* db.query(models.Product) - Product modelini query orqali chaqiramiz.
* .filter(models.Product.price >= min_price) - narxni minimal qiymatga tekshiramiz.
* .filter(models.Product.name.contains(search)) - nom bo'yicha qidiruv amalga oshiramiz.
* query.offset(skip).limit(limit).all() - skip va limit parametrlarini qo'llaymiz.

* URL misol: http://localhost:8000/products/?min_price=100&search=laptop&skip=0&limit=5

## Xulosa
Ushbu darsda, query parameters, filters, va search orqali ma'lumotlarni qanday olish va saralash mumkinligini ko'rdik. Ushbu usullar har qanday murakkab backend tizimlarda foydalanuvchilarga kerakli ma'lumotlarni topish va ko'rsatish imkoniyatini beradi. Katta hajmdagi ma'lumotlar bilan ishlashda ushbu usullar samarali bo'ladi.


---------------------------------------------------------------------------------------------------------


# Sayohat Agentligi uchun API
Keling, sayohat agentligi sayti uchun API yarataylik. Ushbu saytning asosiy modellari quyidagicha bo'ladi:

* Destination - Sayohat manzillari (nomi, tavsifi, narxi, toifasi).
* Category - Sayohat toifalari (nomi).
* Review - Foydalanuvchilar fikri (manzilga tegishli).

## Step 1: database.py faylini yaratish
```python
# database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
```

## Step 2: models.py faylini yaratish
```python
# models.py

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
```
## Step 3: schemas.py faylini yaratish
```python
# schemas.py

from pydantic import BaseModel
from typing import List, Optional

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
    category: Optional['Category']
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

```
## Step 4: main.py faylini yaratish
```python
# main.py

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional

from database import SessionLocal, engine
import models
import schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create Destination
@app.post("/destinations/", response_model=schemas.Destination)
def create_destination(destination: schemas.DestinationCreate, db: Session = Depends(get_db)):
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

# Get Destinations with optional filtering and search
@app.get("/destinations/", response_model=List[schemas.Destination])
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
@app.post("/reviews/", response_model=schemas.Review)
def create_review(review: schemas.ReviewCreate, destination_id: int, db: Session = Depends(get_db)):
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
@app.get("/categories/", response_model=List[schemas.Category])
def read_categories(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(models.Category).offset(skip).limit(limit).all()

# Create Category
@app.post("/categories/", response_model=schemas.Category)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    db_category = models.Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

```

### Tushuntirish
1. Filtering: read_destinations endpointida narx (min_price va max_price), toifalar (category_id), va matnli qidiruv (search) orqali filtering imkoniyati berilgan. filter metodidan foydalanib, kerakli mezonlarni query ga qo'shib ketiladi.

2. Search: name.contains(search) orqali qidiruv amalga oshiriladi. Bu metod matnli maydonlar ichida qidiruvni bajaradi.

3. Query Parameters: skip, limit, min_price, max_price, search, va category_id kabi query parametrlari HTTP so'rovlariga qo'shilib, ma'lumotlarni saralash va chegaralash uchun ishlatiladi.

## Xulosa
Ushbu darsda query parametrlar orqali filtering, full-text search, va ORM orqali kompleks querylarni yozishni o'rgandik. Kichik bir sayohat agentligi uchun API yaratdik va unda foydalanuvchilarni qiziqtiradigan joylarni izlash, saralash imkoniyatlarini ko'rsatdik. Bu mavzular har qanday rivojlangan backend tizimlarda ma'lumotlar bilan ishlashda muhim ahamiyatga ega.