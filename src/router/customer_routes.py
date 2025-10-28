from fastapi import APIRouter
from src.services.customers import (
    fetch_customers,
    fetch_customer_by_id,
    register_new_customer,
    update_customer as update_customer_repo,
    delete_customer as delete_customer_repo,
)
from src.schemas.customers import CustomerCreate, CustomerUpdate

router = APIRouter(prefix="/customers", tags=["customers"])


@router.get("/")
async def get_customers():
    customers = await fetch_customers()
    return {"customers": customers}


@router.get("/{customer_id}")
async def get_customer(customer_id: int):
    customer = await fetch_customer_by_id(customer_id)
    if customer:
        return {"customer": customer}
    return {"error": "Customer not found"}, 404


@router.post("/")
async def create_customer(customer: CustomerCreate):
    new_customer = await register_new_customer(
        name=customer.name,
        email=customer.email,
        phone=customer.phone,
        address=customer.address,
        nickname=customer.nickname,
    )
    return {"customer": new_customer}


@router.put("/{customer_id}")
async def update_customer(customer_id: int, customer: CustomerUpdate):
    updated_customer = await update_customer_repo(
        customer_id=customer_id,
        name=customer.name,
        email=customer.email,
        phone=customer.phone,
        address=customer.address,
        nickname=customer.nickname,
    )
    if updated_customer:
        return {"customer": updated_customer}
    return {"error": "Customer not found"}, 404


@router.delete("/{customer_id}")
async def delete_customer(customer_id: int):
    result = await delete_customer_repo(customer_id)
    if result:
        return {"message": "Customer deleted successfully"}
    return {"error": "Customer not found"}, 404
