import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import  User
from src.schemas import UserModel
from src.repository.users import (
    get_user_by_email,
    create_user,
)


class TestUserRepositoryUsers(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    async def test_get_user_by_email(self):
        user = User()
        self.session.query().filter(User.email == "test").first.return_value = user
        result = await get_user_by_email(email="test", db=self.session)
        self.assertEqual(result, user)

    async def test_get_user_by_email_invalid_email(self):
        self.session.query().filter(User.email == "test").first.return_value = None
        result = await get_user_by_email(email="test", db=self.session)
        self.assertIsNone(result)

    async def test_create_user(self):
        user = UserModel(
            username="test_user",
            email="test@test.com",
            password="PASSWORD"
        )
        self.session.query().filter().all.return_value = user
        result = await create_user(body=user, db=self.session)
        self.assertEqual(result.username, user.username)
        self.assertEqual(result.email, user.email)
        self.assertEqual(result.password, user.password)
        self.assertTrue(hasattr(result, "id"))


if __name__ == '__main__':
    unittest.main()
