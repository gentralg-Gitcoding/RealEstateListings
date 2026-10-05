from typing import Optional

from fastapi import APIRouter

# User files
from services.listing_service import search_listings
from schemas.listings import SearchResult, Listing


router = APIRouter()

@router.get("/")
def root():
    return {"message": "Real Estate Listings API is running!"}

@router.get("/test-listing", response_model=list[Listing])
def test_listing():
    return [Listing (
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
    )]

@router.get("/listings", response_model=SearchResult)
async def get_listings(
    minPrice: Optional[float] = None, 
    maxPrice: Optional[float] = None,
    minBeds: Optional[int] = None,
    city: Optional[str] = None,
    keyword: Optional[str] = None,
    page: int = 1,
    pageSize: int = 10,
    targetBudget: Optional[float] = None
):
    return await search_listings(
        minPrice=minPrice, 
        maxPrice=maxPrice,
        minBeds=minBeds,
        city=city,
        keyword=keyword,
        page=page,
        pageSize=pageSize,
        targetBudget=targetBudget
    )