from datetime import datetime
from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from src.models.base_model import Base


class CustomerModel(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(120), unique=True)
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    address: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )
    nickname: Mapped[str | None] = mapped_column(String(50), nullable=True)
