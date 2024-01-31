from fastapi import Depends, APIRouter, Path, HTTPException, status

from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import Contact
from src.schemas import ContactModel


router = APIRouter(prefix='/contacts', tags=["contacts"])


@router.post("/")
async def create_contact(contact: ContactModel, db: Session = Depends(get_db)):
    new_contact = Contact(name=contact.name, last_name=contact.last_name, email=contact.email, phone_no=contact.phone_no, date_of_birth=contact.date_of_birth, description=contact.description)
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return new_contact


@router.get("/")
async def read_contacts(db: Session = Depends(get_db)):
    contacts = db.query(Contact).all()
    return contacts


@router.get("/{contact_id}")
async def read_contact(contact_id: int = Path(description="The ID of the contact to get", gt=0), db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.put("/{contact_id}")
async def update_contact(updated_contact: ContactModel, contact_id: int = Path(description="The ID of the contact to edit", gt=0), db: Session = Depends(get_db)):

    contact_to_update = db.query(Contact).filter(Contact.id == contact_id).first()

    if not contact_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")

    for key, value in updated_contact.dict(exclude_unset=True).items():
        setattr(contact_to_update, key, value)

    db.commit()
    db.refresh(contact_to_update)
    return contact_to_update


@router.delete("/{contact_id}")
async def delete_contact(contact_id: int = Path(description="The ID of the contact to delete", gt=0), db: Session = Depends(get_db)):

    contact_to_delete = db.query(Contact).filter(Contact.id == contact_id).first()

    if not contact_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")

    db.delete(contact_to_delete)
    db.commit()

    return {"message": "Contact deleted successfully"}
