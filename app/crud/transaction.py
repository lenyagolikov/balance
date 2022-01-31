from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import Transaction


async def get(
    db: AsyncSession, user_id: int, limit: int, offset: int
) -> list[Transaction]:
    transactions = await db.execute(
        select(Transaction)
        .where(Transaction.user_id == user_id)
        .order_by(Transaction.at_created.desc())
    )

    transactions = transactions.scalars().all()

    return transactions[offset - 1 : offset + limit - 1]
