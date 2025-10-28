from pydantic import BaseModel


class CustomerCreate(BaseModel):
    name: str
    email: str
    address: str | None = None
    phone: str | None = None
    nickname: str | None = None


class CustomerUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    address: str | None = None
    phone: str | None = None
    nickname: str | None = None
