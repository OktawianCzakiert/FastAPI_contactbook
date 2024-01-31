from fastapi import Depends, APIRouter, Path, HTTPException, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import ContactModel
from src.repository import contacts as repository_contacts


router = APIRouter(prefix='/contacts', tags=["contacts"])


@router.post("/")
async def create_contact(contact: ContactModel, db: Session = Depends(get_db)):

    return await repository_contacts.create_contact(contact, db)


@router.get("/")
async def read_contacts(db: Session = Depends(get_db)):

    contacts = await repository_contacts.read_contacts(db)
    return contacts


@router.get("/{contact_id}")
async def read_contact(contact_id: int = Path(description="The ID of the contact to get", gt=0), db: Session = Depends(get_db)):

    contact = await repository_contacts.read_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.put("/{contact_id}")
async def update_contact(updated_contact: ContactModel, contact_id: int = Path(description="The ID of the contact to edit", gt=0), db: Session = Depends(get_db)):

    contact = await repository_contacts.update_contact(updated_contact, contact_id, db)
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.delete("/{contact_id}")
async def delete_contact(contact_id: int = Path(description="The ID of the contact to delete", gt=0), db: Session = Depends(get_db)):

    contact = await repository_contacts.delete_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact
