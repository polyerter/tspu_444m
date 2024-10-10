from sqlalchemy.orm import Session
import models
import schemas


def create_wallet(db: Session, wallet: schemas.WalletCreate):
    db_wallet = models.Wallet(
        user_id=wallet.user_id, 
        currency=wallet.currency,
        )
    db.add(db_wallet)
    db.commit()
    db.refresh(db_wallet)
    return db_wallet




