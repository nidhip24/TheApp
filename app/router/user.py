from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import User, UserCreate
from crud import create_user, get_user
import logging

router = APIRouter(prefix="/user", tags=["Users"])

# Configure logging
logging.basicConfig(
    filename='./logs/app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


@router.post("/", response_model=User)
async def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = create_user(db, user)
        logging.info(f"User created, ID: {db_user.id}, Email: {db_user.email}")
        return db_user
    except Exception as e:
        logging.error(f"Error creating user: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{user_id}", response_model=User)
async def retrieve_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if user is None:
        logging.warning(f"User not found - ID: {user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    logging.info(f"User retrieved - ID: {user_id}")
    return user
