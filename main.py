from fastapi import FastAPI, Query, Depends, Path, status, HTTPException

from sqlalchemy.orm import Session
from src.database.db import get_db
from src.database.models import Contact
from src.schemas import ContactModel

app = FastAPI()


@app.post("/contacts")
async def create_contact(contact: ContactModel, db: Session = Depends(get_db)):
    new_contact = Contact(name=contact.name, last_name=contact.last_name, email=contact.email, phone_no=contact.phone_no, date_of_birth=contact.date_of_birth, description=contact.description)
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return new_contact


@app.get("/contacts")
async def read_notes(skip: int = 0, db: Session = Depends(get_db)):
    contacts = db.query(Contact).offset(skip).all()
    return contacts


@app.get("/contact/{contact_id}")
async def read_contact(contact_id: int = Path(description="The ID of the contact to get", gt=0), db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
    return contact
