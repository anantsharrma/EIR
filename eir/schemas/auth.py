
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class PatientRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=12, max_length=128)
    patient_id: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: str
    email: EmailStr
    role: str
    is_active: bool
    patient_id: str | None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    csrf_token: str
    user: UserResponse
