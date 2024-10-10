from fastapi import Depends, FastAPI, HTTPException

from database import SessionLocal, engine
from sqlalchemy.orm import Session

import models
import schemas
import crud
from db import get_db 

from sqlalchemy.exc import IntegrityError
from helpers import generate_token
import datetime
from auth_service import user_auth


models.Base.metadata.create_all(bind=engine)



app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post('/registration')
def registration(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user_old = db.query(models.User).filter(models.User.email == user.email).first()

    if user_old:
        raise HTTPException(status_code=400, detail="Email должен быть уникальным")
       
    try:
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
    except (IntegrityError,) as e:
        return {
            'error': 'Email должен быть уникальным'
        }
    except (Exception,) as e:
        print(e)
        
        return {
            'error': 'Что-то пошло не так'
        }


@app.get("/users")
def users(email: str, db: Session = Depends(get_db)):
    return db.query(models.User).filter(models.User.email == email).all()


@app.post("/auth")
def auth(email: str, password: str, db: Session = Depends(get_db)):
    now_time = datetime.datetime.now()

    db_user_log = models.UserLoggin(
        email=email, 
        created_at=now_time,
    )

    db.add(db_user_log)
    db.commit()
    db.refresh(db_user_log)

    later_time = now_time - datetime.timedelta(minutes=5)

    user_logs = db.query(models.UserLoggin).filter(
        models.UserLoggin.email == email,
        models.UserLoggin.created_at >= later_time,
    ).all()

    limit = 5
    if len(user_logs) >= limit:
        raise HTTPException(status_code=404, detail=f'Rate limit {limit}')

    fake_hashed_password = password + "notreallyhashed"

    user = db.query(models.User).filter(
        models.User.email == email,
        models.User.password == fake_hashed_password
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_token = generate_token()
    user.token = new_token

    db.commit()
    db.refresh(user)

    return user


@app.post("/restore_password")
def restore_password(email: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.email == email,
    ).first()

    restore_token = generate_token()
    user.restore_token = restore_token
    db.commit()
    db.refresh(user)

    return {
        'restore_token': restore_token,
    }


@app.post("/restore_account")
def restore_account(
        restore_token: str, 
        new_password: str, 
        new_password_confirm: str, 
        db: Session = Depends(get_db),
    ):
    user = db.query(models.User).filter(
        models.User.restore_token == restore_token,
    ).first()

    if not user:
        raise HTTPException(status_code=400, detail='User not found')
    
    if new_password != new_password_confirm:
        raise HTTPException(status_code=400, detail='Пароли не совпадают')

    fake_hashed_password = new_password + "notreallyhashed"
    user.password = fake_hashed_password
    user.restore_token = None

    db.commit()
    db.refresh(user)

    return {
        'status': True,
    }


@app.post("/wallet", response_model=schemas.WalletCreate)
async def create_wallet(
        wallet: schemas.WalletCreate, 
        db: Session = Depends(get_db),
        user = Depends(user_auth),  # noqa: inject user to check auth
    ):

    wallet.user_id = user.id

    return crud.create_wallet(db=db, wallet=wallet)
