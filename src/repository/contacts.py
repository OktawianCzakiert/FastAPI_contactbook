from fastapi import Depends, Path
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import Contact
from src.schemas import ContactModel


async def create_contact(contact: ContactModel, db: Session = Depends(get_db)):

    new_contact = Contact(name=contact.name, last_name=contact.last_name, email=contact.email, phone_no=contact.phone_no, date_of_birth=contact.date_of_birth, description=contact.description)
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)

    return new_contact


async def read_contacts(db: Session = Depends(get_db)):

    return db.query(Contact).all()


async def read_contact(contact_id: int = Path(description="The ID of the contact to get", gt=0), db: Session = Depends(get_db)):

    return db.query(Contact).filter(Contact.id == contact_id).first()


async def update_contact(updated_contact: ContactModel, contact_id: int = Path(description="The ID of the contact to edit", gt=0), db: Session = Depends(get_db)):

    contact_to_update = db.query(Contact).filter(Contact.id == contact_id).first()

    if contact_to_update:
        for key, value in updated_contact.dict(exclude_unset=True).items():
            setattr(contact_to_update, key, value)

        db.commit()
        db.refresh(contact_to_update)

    return contact_to_update


async def delete_contact(contact_id: int = Path(description="The ID of the contact to delete", gt=0), db: Session = Depends(get_db)):

    contact_to_delete = db.query(Contact).filter(Contact.id == contact_id).first()

    if contact_to_delete:
        db.delete(contact_to_delete)
        db.commit()

    return {"message": "Contact deleted successfully"}