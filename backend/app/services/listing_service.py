from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import select, func

# User files
from database.connection import SessionLocal
from database.models import Listing as ListingModel
from schemas.listings import Listing

async def search_listings(
    minPrice=None, 
    maxPrice=None,
    minBeds=None,
    city=None,
    keyword=None,
    page=1,
    pageSize=10,
    targetBudget=None
):
    if page <= 0 or pageSize <= 0:
        raise HTTPException(
            status_code=400,
            detail="Page and Page Size must be greater than 0."
        )

    if minPrice != None and maxPrice != None and minPrice >= maxPrice:
        raise HTTPException(
            status_code=400,
            detail="Invalid price range. Minimum price cannot be greater than maximum price."
        )

    async with SessionLocal() as session:

        query = select(ListingModel)

        # Filter Logic
        if minPrice is not None:
            query = query.where(ListingModel.price >= minPrice)

        if maxPrice is not None:
            query = query.where(ListingModel.price <= maxPrice)

        if minBeds is not None:
            query = query.where(ListingModel.bedrooms >= minBeds)

        if city is not None:
            query = query.where(ListingModel.city.ilike(f"%{city}%"))

        if keyword is not None:
            query = query.where(ListingModel.description.ilike(f"%{keyword}%"))

        # SQL Count on query for Visualization of Total
        count_query = select(func.count()).select_from(query.subquery())
        count_result = await session.execute(count_query)
        total = count_result.scalar_one()

        result = await session.execute(query)
        listings = result.scalars().all()

        # Score calculation
        scored_listings = []
        for listing in listings:

            budget_score = 1.0

            if targetBudget is not None:
                diff = abs(listing.price - targetBudget)
                budget_score = max(0, 1 - diff / targetBudget)

            now_time = datetime.now()
            listed_date = datetime.fromisoformat(listing.listedDate)

            age = now_time - listed_date
            age_seconds = age.total_seconds()
            thirty_days = 30 * 24 * 60 * 60

            recency_score = max(0, 1 - age_seconds / thirty_days)

            final_score = (budget_score + recency_score) / 2
            scored_listings.append({
                "listing": listing,
                "score": final_score
            })

        scored_listings.sort(key=lambda item: item["score"], reverse=True)

        # Pagination
        offset = (page - 1) * pageSize
        paginated_listings = scored_listings[offset:offset + pageSize]

        # Convert our ORM object back into data + score dicts for SearchResult
        data = []
        for item in paginated_listings:
            listing = Listing.model_validate(item["listing"])

            data.append({
                **listing.model_dump(),
                "score": item["score"]
            })


        return {
            "data": data,
            "total":total, 
            "page":page, 
            "pageSize":pageSize
        }