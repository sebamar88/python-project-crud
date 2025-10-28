from src.models.customer_model import CustomerModel
from src.repositories.customer_repository import (
    get_customer,
    create_customer,
    fetch_all_customers,
    update_customer as repo_update_customer,
    delete_customer as repo_delete_customer,
)


async def register_new_customer(
    name: str,
    email: str,
    phone: str | None = None,
    address: str | None = None,
    nickname: str | None = None,
) -> CustomerModel:
    # Lógica adicional antes de crear el cliente puede ir aquí
    new_customer = await create_customer(
        name=name,
        email=email,
        phone=phone,
        address=address,
        nickname=nickname,
    )
    return new_customer


async def fetch_customers() -> list[CustomerModel]:
    # Ejemplo de función para obtener múltiples clientes
    customers = await fetch_all_customers()
    return customers


async def fetch_customer_by_id(customer_id: int) -> CustomerModel | None:
    # Ejemplo de función para obtener un cliente por ID
    customer = await get_customer(customer_id)
    return customer


async def update_customer(
    customer_id: int,
    name: str | None = None,
    email: str | None = None,
    phone: str | None = None,
    address: str | None = None,
    nickname: str | None = None,
) -> CustomerModel | None:
    updated_customer = await repo_update_customer(
        customer_id=customer_id,
        name=name,
        email=email,
        phone=phone,
        address=address,
        nickname=nickname,
    )
    return updated_customer


async def delete_customer(customer_id: int) -> bool:
    result = await repo_delete_customer(customer_id)
    return result
