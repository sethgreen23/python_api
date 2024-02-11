
from fastapi import FastAPI, Body, APIRouter, status, HTTPException, Response, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..database import get_db
from .. import schema, models, utils

router = APIRouter(prefix="/users")
# user end points
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.UserOut)
def create_user(user: schema.CreateUser, db: Session = Depends(get_db)):
    new_user = models.User(**user.dict())
    hashed_password = utils.hash(new_user.password)
    new_user.password = hashed_password
    # test if the email already exists
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User with email {new_user.email} already exist")
        
    return new_user

@router.get("/{id}", response_model=schema.UserOut)
def get_users(id:int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    print(user)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"User with id {id} doesn't exist!")
    return user
