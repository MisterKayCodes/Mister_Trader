from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.account import AccountCreate, AccountRead
from app.services import account_service
# Rule 13: Standard Auth Imports
from app.api.v1.deps import get_current_user
from app.models.user import User

router = APIRouter(tags=["accounts"])

# Rule 13: Changed "/" to "" for clean 2026 URL structure
@router.post("", response_model=AccountRead, status_code=status.HTTP_201_CREATED)
def create_account(
    account: AccountCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) # Rule 14: Security Guard
):
    try:
        return account_service.create_account(
            db=db,
            user_id=current_user.id, # Rule 1: Use verified ID from token
            name=account.name
        )
    except ValueError as e:
        if str(e) == "MAX_ACCOUNTS_REACHED":
            raise HTTPException(status_code=400, detail="Maximum number of accounts reached")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("", response_model=List[AccountRead])
def list_accounts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Rule 14: Users can only see their OWN accounts
    return account_service.list_accounts(db, user_id=current_user.id)

@router.get("/{account_id}", response_model=AccountRead)
def get_account(
    account_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Rule 14: Service now requires user_id to verify ownership
    account = account_service.get_account(db, account_id, user_id=current_user.id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found or unauthorized")
    return account

@router.put("/{account_id}", response_model=AccountRead)
def update_account(
    account_id: int, 
    account: AccountCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    updated = account_service.update_account(
        db, 
        account_id=account_id, 
        user_id=current_user.id, 
        name=account.name
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Account not found or unauthorized")
    return updated

@router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_account(
    account_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Rule 14: Verify ownership before allowing deletion
    success = account_service.delete_account(db, account_id, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Account not found or unauthorized")
    return None
