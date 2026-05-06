from datetime import date

from sqlalchemy import select

from src.database.db import AsyncSessionLocal, Base, engine
from src.models.contact import Contact


TEST_CONTACTS = [
    Contact(
        first_name="Іван",
        last_name="Франко",
        email="franko@example.com",
        phone="+1234567890",
        birthday=date(1990, 5, 10),
        additional_data="Seed contact 1",
    ),
    Contact(
        first_name="Сергій",
        last_name="Корольов",
        email="korolov@example.com",
        phone="+1987654321",
        birthday=date(1992, 5, 14),
        additional_data="Seed contact 2",
    ),
    Contact(
        first_name="Григорій",
        last_name="Сковорода",
        email="skovoroda@example.com",
        phone="+380501112233",
        birthday=date(2001, 5, 18),
        additional_data="Seed contact 3",
    ),
]


async def seed_contacts() -> None:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Contact.email))
        existing_emails = set(result.scalars().all())

        contacts_to_insert = [
            contact for contact in TEST_CONTACTS if contact.email not in existing_emails
        ]

        if not contacts_to_insert:
            return

        session.add_all(contacts_to_insert)
        await session.commit()


if __name__ == "__main__":
    import asyncio

    asyncio.run(seed_contacts())
