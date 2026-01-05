from sqlalchemy.orm import Session
from app.models.account import Account

MAX_ACCOUNTS_PER_USER = 6


def create_account(db: Session, user_id: int, name: str) -> Account:
    count = db.query(Account).filter(Account.user_id == user_id).count()
    if count >= MAX_ACCOUNTS_PER_USER:
        raise ValueError("MAX_ACCOUNTS_REACHED")

    account = Account(user_id=user_id, name=name)
    db.add(account)
    db.commit()
    db.refresh(account)
    return account


def list_accounts(db: Session, user_id: int):
    return db.query(Account).filter(Account.user_id == user_id).all()


def get_account(db: Session, account_id: int):
    return db.query(Account).filter(Account.id == account_id).first()


def update_account(db: Session, account_id: int, name: str):
    account = get_account(db, account_id)
    if not account:
        return None

    account.name = name
    db.commit()
    db.refresh(account)
    return account


def delete_account(db: Session, account_id: int) -> bool:
    account = get_account(db, account_id)
    if not account:
        return False

    db.delete(account)
    db.commit()
    return True
