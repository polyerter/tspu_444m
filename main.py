from fastapi import Depends, FastAPI, HTTPException

from database import SessionLocal, engine
from sqlalchemy.orm import Session

import models
import schemas


models.Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post('/registration')
def registration(user: schemas.UserCreate, db: Session = Depends(get_db)):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(
        email=user.email, 
        username=user.username, 
        password=fake_hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

@app.get("/users")
def users(email: str, db: Session = Depends(get_db)):
    return db.query(models.User).filter(models.User.email == email).all()
