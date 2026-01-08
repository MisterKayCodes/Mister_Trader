from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from app.models.trade_draft import TradeDraft
from app.models.account import Account # Needed for ownership check

def create_draft(db: Session, user_id: int, draft_in: dict):
    # Rule 14: Verify Account Ownership
    stmt = select(Account).where(and_(Account.id == draft_in["account_id"], Account.user_id == user_id))
    account = db.scalar(stmt)
    if not account:
        raise ValueError("UNAUTHORIZED_ACCOUNT")

    db_draft = TradeDraft(**draft_in)
    db.add(db_draft)
    db.commit()
    db.refresh(db_draft)
    return db_draft

def list_drafts(db: Session, user_id: int, account_id: int):
    # Rule 14: Join with Account to filter by user_id
    stmt = select(TradeDraft).join(Account).where(
        and_(TradeDraft.account_id == account_id, Account.user_id == user_id)
    )
    return db.scalars(stmt).all()

def delete_draft(db: Session, user_id: int, draft_id: int) -> bool:
    stmt = select(TradeDraft).join(Account).where(
        and_(TradeDraft.id == draft_id, Account.user_id == user_id)
    )
    db_draft = db.scalar(stmt)
    if not db_draft:
        return False
    db.delete(db_draft)
    db.commit()
    return True
