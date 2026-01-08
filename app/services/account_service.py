from sqlalchemy.orm import Session
from sqlalchemy import select, and_, func
from app.models.account import Account

# Rule 1: System constraint for known state
MAX_ACCOUNTS_PER_USER = 6

def create_account(db: Session, user_id: int, name: str) -> Account:
    # Rule 13: Using modern SQLAlchemy 2.0 count logic
    count = db.scalar(select(func.count()).select_from(Account).where(Account.user_id == user_id))
    
    if count >= MAX_ACCOUNTS_PER_USER:
        raise ValueError("MAX_ACCOUNTS_REACHED")

    account = Account(user_id=user_id, name=name)
    db.add(account)
    db.commit()
    db.refresh(account)
    return account

def list_accounts(db: Session, user_id: int):
    # Rule 14: Privacy - strictly filter by the authenticated user_id
    stmt = select(Account).where(Account.user_id == user_id)
    return db.execute(stmt).scalars().all()

def get_account(db: Session, account_id: int, user_id: int):
    """Rule 6: No guessing - find the specific account for the specific user."""
    stmt = select(Account).where(
        and_(Account.id == account_id, Account.user_id == user_id)
    )
    return db.execute(stmt).scalars().first()

def update_account(db: Session, account_id: int, user_id: int, name: str):
    # Rule 14: Verify ownership before allowing an update
    account = get_account(db, account_id, user_id)
    if not account:
        return None

    account.name = name
    db.commit()
    db.refresh(account)
    return account

def delete_account(db: Session, account_id: int, user_id: int) -> bool:
    # Rule 14: Verify ownership before allowing deletion
    account = get_account(db, account_id, user_id)
    if not account:
        return False

    db.delete(account)
    db.commit()
    return True

 