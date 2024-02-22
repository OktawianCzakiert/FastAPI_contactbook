from fastapi import Depends, Path
from sqlalchemy.orm import Session
from sqlalchemy import and_

from src.database.db import get_db
from src.database.models import Contact, User
from src.schemas import ContactModel


async def create_contact(contact: ContactModel, user: User, db: Session = Depends(get_db)):
    """
    Creates a new contact for the specified user.

    Args:
        contact (ContactModel): The contact details.
        user (User): The user creating the contact.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        Contact: The newly created contact.
    """
    new_contact = Contact(name=contact.name, last_name=contact.last_name, email=contact.email, phone_no=contact.phone_no, date_of_birth=contact.date_of_birth, description=contact.description, user_id=user.id)
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)

    return new_contact


async def read_contacts(user: User, db: Session = Depends(get_db)):
    """
    Retrieves all contacts for the specified user.

    Args:
        user (User): The user to retrieve contacts for.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        list: List of contacts belonging to the user.
    """

    return db.query(Contact).filter(Contact.user_id == user.id).all()


async def read_contact(user: User, contact_id: int = Path(description="The ID of the contact to get", gt=0),  db: Session = Depends(get_db)):
    """
    Retrieves a specific contact for the specified user by contact ID.

    Args:
        user (User): The user to retrieve the contact for.
        contact_id (int): The ID of the contact to retrieve.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        Contact: The requested contact.
    """
    return db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()


async def update_contact(user: User, updated_contact: ContactModel, contact_id: int = Path(description="The ID of the contact to edit", gt=0),  db: Session = Depends(get_db)):
    """
    Updates a specific contact for the specified user by contact ID.

    Args:
        user (User): The user updating the contact.
        updated_contact (ContactModel): The updated contact details.
        contact_id (int): The ID of the contact to update.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        Contact: The updated contact.
    """
    contact_to_update = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()

    if contact_to_update:
        for key, value in updated_contact.dict(exclude_unset=True).items():
            setattr(contact_to_update, key, value)

        db.commit()
        db.refresh(contact_to_update)

    return contact_to_update


async def delete_contact(user: User, contact_id: int = Path(description="The ID of the contact to delete", gt=0), db: Session = Depends(get_db)):
    """
    Deletes a specific contact for the specified user by contact ID.

    Args:
        user (User): The user deleting the contact.
        contact_id (int): The ID of the contact to delete.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        dict: A message confirming successful deletion.
    """
    contact_to_delete = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()

    if contact_to_delete:
        db.delete(contact_to_delete)
        db.commit()

    return contact_to_delete
    # return {"message": "Contact deleted successfully"}
