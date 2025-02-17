from sqlalchemy.orm import Session
from models import UserDB
from schemas import UserCreate


def create_user(db: Session, user: UserCreate):
    db_user = UserDB(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int):
    return db.query(UserDB).filter(UserDB.id == user_id).first()
