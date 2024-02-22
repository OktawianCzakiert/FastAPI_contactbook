import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session
from sqlalchemy import and_

from src.database.models import Contact, User
from src.schemas import ContactModel
from src.repository.contacts import (
    create_contact,
    read_contacts,
    read_contact,
    update_contact,
    delete_contact
)


class TestUnitRepositoryContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    async def test_create_contact(self):
        contact = ContactModel(
            name="test name",
            last_name="test last name",
            email="test@test.com",
            phone_no="123123123",
            date_of_birth="2024-02-20"
        )

        result = await create_contact(contact=contact, user=self.user, db=self.session)
        self.assertEqual(result.name, contact.name)
        self.assertEqual(result.last_name, contact.last_name)
        self.assertEqual(result.email, contact.email)
        self.assertEqual(result.phone_no, contact.phone_no)
        self.assertEqual(result.date_of_birth, contact.date_of_birth)
        self.assertTrue(hasattr(result, "id"))

    async def test_read_contacts(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter(Contact.user_id == self.user.id).all.return_value = contacts
        result = await read_contacts(user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_read_contact_found(self):
        contact = Contact()
        self.session.query().filter(and_(Contact.id == 1, Contact.user_id == self.user.id)).first.return_value = contact
        result = await read_contact(user=self.user, contact_id=1, db=self.session)
        self.assertEqual(result, contact)

    async def test_read_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await read_contact(user=self.user, contact_id=1, db=self.session)
        self.assertIsNone(result)

    async def test_update_contact_found(self):
        updated_contact = ContactModel(
            name="test name",
            last_name="test last name",
            email="test@test.com",
            phone_no="123123123",
            date_of_birth="2024-02-20"
        )
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        self.session.commit.return_value = None
        result = await update_contact(user=self.user, updated_contact=updated_contact,contact_id=1, db=self.session)
        self.assertEqual(result, contact)

    async def test_update_contact_not_found(self):
        updated_contact = ContactModel(
            name="test name",
            last_name="test last name",
            email="test@test.com",
            phone_no="123123123",
            date_of_birth="2024-02-20"
        )
        self.session.query().filter().first.return_value = None
        self.session.commit.return_value = None
        result = await update_contact(user=self.user, updated_contact=updated_contact,contact_id=1, db=self.session)
        self.assertIsNone(result)

    async def test_delete_contact_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await delete_contact(user=self.user, contact_id=1, db=self.session)
        self.assertEqual(result, contact)

    async def test_delete_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await delete_contact(user=self.user, contact_id=1, db=self.session)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
