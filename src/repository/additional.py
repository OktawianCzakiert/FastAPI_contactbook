from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, extract
from datetime import datetime, timedelta
import calendar

from src.database.db import get_db
from src.database.models import Contact, User


async def read_birthday(user: User, db: Session = Depends(get_db)):
    """
    Retrieve contacts whose birthdays are within the next 7 days for a given user.

    Args:
        user (User): The user for whom to retrieve contacts.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        List[Contact]: A list of contacts whose birthdays are within the next 7 days.
    """
    today = datetime.now().date()
    last_day_in_month = calendar.monthrange(today.year, today.month)[1]
    end_date = today + timedelta(days=7)

    contacts = db.query(Contact).filter(
        or_(
            and_(
                Contact.user_id == user.id,
                extract("month", Contact.date_of_birth) == today.month,
                extract("day", Contact.date_of_birth) >= today.day,
                or_(
                    extract("day", Contact.date_of_birth) <= end_date.day,
                    extract("day", Contact.date_of_birth) <= last_day_in_month
                ),
            ),
            and_(
                Contact.user_id == user.id,
                extract("month", Contact.date_of_birth) == (today + timedelta(days=7)).month,
                extract("day", Contact.date_of_birth) <= (end_date - timedelta(days=7)).day
            )
        )
    ).all()

    return contacts


async def search_by_phrase(phrase: str, user: User, db: Session = Depends(get_db)):
    """
    Retrieve contacts for a given user that match a given phrase in their name, last name, or email.

    Args:
        phrase (str): The phrase to search for in the contacts' name, last name, or email.
        user (User): The user for whom to retrieve contacts.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        List[Contact]: A list of contacts matching the given search phrase.
    """
    contacts = db.query(Contact).filter(
        and_(
            Contact.user_id == user.id,
            or_(
                Contact.name.like(f"%{phrase}%"),
                Contact.last_name.like(f"%{phrase}%"),
                Contact.email.like(f"%{phrase}%")
            )
        )
    ).all()

    return contacts
