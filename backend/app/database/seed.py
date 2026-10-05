import asyncio
import json
from pathlib import Path

#User files
from database.models import Base, Listing
from database.connection import SessionLocal, engine
from database.models import Listing

DATA_FILE = Path(__file__).parent.parent/"data"/"sample_listings.json"

def load_listings():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

async def test_connection():
    async with engine.connect() as connection:
        print("Successfully connected to PostgreSQL!")

async def create_tables():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

async def test_insert():
    async with SessionLocal() as session:
        listing = Listing(
            id="123",
            source="TestSource",
            address="123 Sesame Street",
            city="Elmos World",
            state="EW",
            zip="01234",
            price=40000,
            bedrooms=3,
            bathrooms=2,
            sqft=2500,
            latitude=54.321,
            longitude=56.789,
            listedDate="2026-09-03",
            status="active",
            description="Won't you tell me how to get. How to get to Sesame Street?"
        )

        session.add(listing)

        await session.commit()

        print("Listing inserted!")

async def seed_database():

    listings = load_listings()

    async with SessionLocal() as session:

        for listing_data in listings:
            listing = Listing(**listing_data)
            session.add(listing)

        await session.commit()

    print(f"Inserted {len(listings)} listings!")

if __name__ == "__main__":
    asyncio.run(seed_database())