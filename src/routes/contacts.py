from fastapi import Depends, APIRouter, Path, HTTPException, status
from sqlalchemy.orm import Session
from fastapi_limiter.depends import RateLimiter

from src.database.db import get_db
from src.database.models import User
from src.schemas import ContactModel
from src.repository import contacts as repository_contacts
from src.services.auth import auth_service

router = APIRouter(prefix='/contacts', tags=["contacts"])


@router.post("/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(RateLimiter(times=2, seconds=30))])
async def create_contact(
        contact: ContactModel,
        db: Session = Depends(get_db),
        current_user: User = Depends(auth_service.get_current_user)
):

    return await repository_contacts.create_contact(contact, current_user, db)


@router.get("/")
async def read_contacts(
        db: Session = Depends(get_db),
        current_user: User = Depends(auth_service.get_current_user)
):

    contacts = await repository_contacts.read_contacts(current_user, db)
    return contacts


@router.get("/{contact_id}")
async def read_contact(
        contact_id: int = Path(description="The ID of the contact to get", gt=0),
        db: Session = Depends(get_db),
        current_user: User = Depends(auth_service.get_current_user)
):

    contact = await repository_contacts.read_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.put("/{contact_id}", dependencies=[Depends(RateLimiter(times=2, seconds=30))])
async def update_contact(
        updated_contact: ContactModel,
        contact_id: int = Path(description="The ID of the contact to edit", gt=0),
        db: Session = Depends(get_db),
        current_user: User = Depends(auth_service.get_current_user)
):

    contact = await repository_contacts.update_contact(updated_contact, contact_id,current_user, db)
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.delete("/{contact_id}", dependencies=[Depends(RateLimiter(times=1, seconds=30))])
async def delete_contact(
        contact_id: int = Path(description="The ID of the contact to delete", gt=0),
        db: Session = Depends(get_db),
        current_user: User = Depends(auth_service.get_current_user)
):

    contact = await repository_contacts.delete_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact
