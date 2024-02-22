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
    """
    Create a new contact.

    Args:
        contact (ContactModel): The contact details.
        db (Session, optional): The database session. Defaults to Depends(get_db).
        current_user (User, optional): The current authenticated user. Defaults to Depends(auth_service.get_current_user).

    Returns:
        ContactModel: The created contact.
    """
    return await repository_contacts.create_contact(contact, current_user, db)


@router.get("/")
async def read_contacts(
        db: Session = Depends(get_db),
        current_user: User = Depends(auth_service.get_current_user)
):
    """
    Read all contacts.

    Args:
        db (Session, optional): The database session. Defaults to Depends(get_db).
        current_user (User, optional): The current authenticated user. Defaults to Depends(auth_service.get_current_user).

    Returns:
        List[ContactModel]: List of contacts.
    """
    contacts = await repository_contacts.read_contacts(current_user, db)
    return contacts


@router.get("/{contact_id}")
async def read_contact(
        contact_id: int = Path(description="The ID of the contact to get", gt=0),
        db: Session = Depends(get_db),
        current_user: User = Depends(auth_service.get_current_user)
):
    """
    Read a specific contact by its ID.

    Args:
        contact_id (int): The ID of the contact to retrieve.
        db (Session, optional): The database session. Defaults to Depends(get_db).
        current_user (User, optional): The current authenticated user. Defaults to Depends(auth_service.get_current_user).

    Raises:
        HTTPException: If contact with given ID is not found.

    Returns:
        ContactModel: The requested contact.
    """
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
    """
    Update a contact by its ID.

    Args:
        updated_contact (ContactModel): The updated contact details.
        contact_id (int): The ID of the contact to edit.
        db (Session, optional): The database session. Defaults to Depends(get_db).
        current_user (User, optional): The current authenticated user. Defaults to Depends(auth_service.get_current_user).

    Raises:
        HTTPException: If contact with given ID is not found.

    Returns:
        ContactModel: The updated contact.
    """
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
    """
    Delete a contact by its ID.

    Args:
        contact_id (int): The ID of the contact to delete.
        db (Session, optional): The database session. Defaults to Depends(get_db).
        current_user (User, optional): The current authenticated user. Defaults to Depends(auth_service.get_current_user).

    Raises:
        HTTPException: If contact with given ID is not found.

    Returns:
        ContactModel: The deleted contact.
    """
    contact = await repository_contacts.delete_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact
