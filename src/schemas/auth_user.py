from pydantic import BaseModel, EmailStr, field_validator


class AuthUserBaseSchema(BaseModel):
    email: EmailStr
    role: str | None = "user"

    @field_validator("role")
    def role_must_be_valid(cls, v):
        if v not in ["user", "admin"]:
            raise ValueError("Invalid role")
        return v


class AuthUserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class AuthUserCreateSchema(AuthUserBaseSchema):
    password: str
    role: str | None = "user"


class AuthUserUpdateSchema(AuthUserBaseSchema):
    password: str | None = None
    role: str | None = None


class AuthUserResponseSchema(AuthUserBaseSchema):
    id: int
    created_at: str
    updated_at: str | None = None

    class Config:
        from_attributes = True
