from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.account import Account
from app.schemas.account import AccountCreate, AccountRead

router = APIRouter(tags=["accounts"])

MAX_ACCOUNTS_PER_USER = 6

@router.post("/", response_model=AccountRead)
def create_account(account: AccountCreate, db: Session = Depends(get_db)):
    # Count existing accounts for the user
    count = db.query(Account).filter(Account.user_id == account.user_id).count()
    if count >= MAX_ACCOUNTS_PER_USER:
        raise HTTPException(status_code=400, detail="Maximum number of accounts reached")
    
    new_account = Account(user_id=account.user_id, name=account.name)
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    return new_account


@router.get("/", response_model=List[AccountRead])
def list_accounts(user_id: int, db: Session = Depends(get_db)):
    accounts = db.query(Account).filter(Account.user_id == user_id).all()
    return accounts

@router.get("/{account_id}", response_model=AccountRead)
def get_account(account_id: int, db: Session = Depends(get_db)):
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


@router.put("/{account_id}", response_model=AccountRead)
def update_account(account_id: int, account_update: AccountCreate, db: Session = Depends(get_db)):
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    account.name = account_update.name
    db.commit()
    db.refresh(account)
    return account

@router.delete("/{account_id}")
def delete_account(account_id: int, db: Session = Depends(get_db)):
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    db.delete(account)
    db.commit()
    return {"detail": "Account deleted successfully"}