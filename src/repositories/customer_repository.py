from src.models.customer_model import CustomerModel
from src.core.database import async_session
from sqlalchemy.sql import text
from sqlalchemy import delete, select
from datetime import datetime, timezone


async def fetch_all_customers() -> list[CustomerModel]:
    async with async_session() as session:
        query = text("SELECT * FROM customers")
        result = await session.execute(query)
        rows = result.fetchall()
        return [CustomerModel(**row._mapping) for row in rows]


async def get_customer(customer_id: int) -> CustomerModel | None:
    async with async_session() as session:
        query = text("SELECT * FROM customers WHERE id = :customer_id")
        result = await session.execute(query, {"customer_id": customer_id})
        row = result.first()
        if row:
            return CustomerModel(**row._mapping)
        return None


async def create_customer(
    name: str,
    email: str,
    phone: str | None = None,
    address: str | None = None,
    nickname: str | None = None,
) -> CustomerModel:
    async with async_session() as session:
        new_customer = CustomerModel(
            name=name,
            email=email,
            phone=phone,
            address=address,
            nickname=nickname,
            created_at=datetime.now(timezone.utc),
        )
        session.add(new_customer)
        await session.commit()
        await session.refresh(new_customer)
        return new_customer


async def delete_customer(customer_id: int) -> bool:
    async with async_session() as session:
        stmt = delete(CustomerModel).where(CustomerModel.id == customer_id)
        result = await session.execute(stmt)
        await session.commit()

        # rowcount sigue existiendo, pero lo casteamos explícitamente
        return bool(getattr(result, "rowcount", 0))


async def update_customer(
    customer_id: int,
    name: str | None = None,
    email: str | None = None,
    phone: str | None = None,
    address: str | None = None,
    nickname: str | None = None,
) -> CustomerModel | None:
    async with async_session() as session:
        customer = await session.get(CustomerModel, customer_id)
        if not customer:
            return None

        if name is not None:
            customer.name = name
        if email is not None:
            customer.email = email
        if phone is not None:
            customer.phone = phone
        if address is not None:
            customer.address = address
        if nickname is not None:
            customer.nickname = nickname

        customer.updated_at = datetime.now(timezone.utc)

        session.add(customer)
        await session.commit()
        await session.refresh(customer)
        return customer
