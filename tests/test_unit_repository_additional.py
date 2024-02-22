import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.repository.additional import (
    read_birthday,
    search_by_phrase,
)


class TestAdditionalRepository(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    async def test_read_birthday(self):

        bday_users = [Contact(), Contact(), Contact()]
        self.session.query().filter(Contact.user_id == self.user.id).all.return_value = bday_users
        result = await read_birthday(user=self.user, db=self.session)
        self.assertEqual(result, bday_users)

    async def test_search_by_phrase(self):
        phrase_users = [Contact(), Contact(), Contact()]
        self.session.query().filter(Contact.user_id == self.user.id).all.return_value = phrase_users
        result = await search_by_phrase(phrase="test", user=self.user, db=self.session)
        self.assertEqual(result, phrase_users)


if __name__ == '__main__':
    unittest.main()
