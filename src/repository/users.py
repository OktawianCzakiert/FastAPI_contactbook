from libgravatar import Gravatar
from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel


async def get_user_by_email(email: str, db: Session) -> User:
    """
    Retrieve a user from the database by email.

    Args:
        email (str): The email address of the user to retrieve.
        db (Session): The SQLAlchemy database session.

    Returns:
        User: The user corresponding to the provided email, if found; otherwise, None.
    """
    return db.query(User).filter(User.email == email).first()


async def create_user(body: UserModel, db: Session) -> User:
    """
    Create a new user and store it in the database.

    Args:
        body (UserModel): The data model representing the user to be created.
        db (Session): The SQLAlchemy database session.

    Returns:
        User: The newly created user.
    """
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)
    new_user = User(**body.dict(), avatar=avatar)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session):
    """
    Update the refresh token for a user.

    Args:
        user (User): The user whose token needs to be updated.
        token (str | None): The new refresh token. Pass None to remove the token.
        db (Session): The SQLAlchemy database session.

    Returns:
        User
    """
    user.refresh_token = token
    db.commit()
    return user


async def confirm_email(email: str, db: Session):
    """
    Confirm a user's email address.

    Args:
        email (str): The email address of the user to confirm.
        db (Session): The SQLAlchemy database session.

    Returns:
        None
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()
    return user


async def update_avatar(email, url: str, db: Session) -> User:
    """
    Update the avatar URL for a user.

    Args:
        email (str): The email address of the user whose avatar URL is to be updated.
        url (str): The new avatar URL.
        db (Session): The SQLAlchemy database session.

    Returns:
        User: The updated user object.
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user
