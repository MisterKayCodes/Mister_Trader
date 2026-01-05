from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.account import AccountCreate, AccountRead
from app.services import account_service

router = APIRouter(tags=["accounts"])


@router.post("/", response_model=AccountRead)
def create_account(account: AccountCreate, db: Session = Depends(get_db)):
    try:
        return account_service.create_account(
            db=db,
            user_id=account.user_id,
            name=account.name
        )
    except ValueError as e:
        if str(e) == "MAX_ACCOUNTS_REACHED":
            raise HTTPException(status_code=400, detail="Maximum number of accounts reached")


@router.get("/", response_model=List[AccountRead])
def list_accounts(user_id: int, db: Session = Depends(get_db)):
    return account_service.list_accounts(db, user_id)


@router.get("/{account_id}", response_model=AccountRead)
def get_account(account_id: int, db: Session = Depends(get_db)):
    account = account_service.get_account(db, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


@router.put("/{account_id}", response_model=AccountRead)
def update_account(account_id: int, account: AccountCreate, db: Session = Depends(get_db)):
    updated = account_service.update_account(db, account_id, account.name)
    if not updated:
        raise HTTPException(status_code=404, detail="Account not found")
    return updated


@router.delete("/{account_id}")
def delete_account(account_id: int, db: Session = Depends(get_db)):
    success = account_service.delete_account(db, account_id)
    if not success:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"detail": "Account deleted successfully"}
