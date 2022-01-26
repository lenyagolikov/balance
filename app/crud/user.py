from sqlalchemy.orm import Session

from app.models.user import User


async def get_user(db: Session, user_id) -> User:
    user = db.query(User).filter(User.id==user_id).first()
    return user
