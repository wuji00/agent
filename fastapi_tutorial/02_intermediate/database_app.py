from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# 1. 数据库设置 (使用 SQLite)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
# check_same_thread=False 仅在 SQLite 中需要
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 2. 数据库模型 (SQLAlchemy Models)
class DBUser(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)

# 创建表
Base.metadata.create_all(bind=engine)

# 3. Pydantic 模式 (Schemas)
class UserCreate(BaseModel):
    email: str

class User(BaseModel):
    id: int
    email: str
    is_active: bool

    # Pydantic v2 配置，允许从 ORM 对象读取数据
    model_config = ConfigDict(from_attributes=True)

# 4. 依赖项 (Dependency)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 5. FastAPI 应用
app = FastAPI()

@app.post("/users/", response_model=User)
def create_user(user: UserCreate, db: Annotated[Session, Depends(get_db)]):
    db_user = db.query(DBUser).filter(DBUser.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = DBUser(email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    db_user = db.query(DBUser).filter(DBUser.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
