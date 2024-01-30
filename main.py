from fastapi import FastAPI, Path
from pydantic import BaseModel

app = FastAPI()


class Contact(BaseModel):
    name: str
    last_name: str
    email: str
    phone_no: str
    date_of_birth: str
    description: str

@app.get("/contacts")
def get_contacts():
    return {"message": "Welcome to FastAPI!"}

@app.get("/contact/{contact_id}")
async def read_contact(contact_id: int = Path(description="The ID of the contact to get", gt=0)):
        return {"contact": contact_id}
