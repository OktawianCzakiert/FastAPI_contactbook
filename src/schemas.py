from datetime import date
from typing import Optional
from pydantic import BaseModel, EmailStr


class ContactModel(BaseModel):
    name: str
    last_name: str
    email: EmailStr
    phone_no: str
    date_of_birth: date
    description: Optional[str] = ""
