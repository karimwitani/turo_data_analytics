import datetime
from pprint import pprint
import sys

from fastapi import FastAPI, HTTPException, Depends

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError


from database import async_session
from models.sqlalchemy_models import Item, Vehicle, BookingSummaries, BookingDetails
from models.search_page_models import TuroSearchRequestModel
from models.daily_pricing_models import DailyPricingRequestModel


# Dependency
async def get_db():
    async with async_session() as session:
        yield session

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Item).where(Item.id == item_id))
    item = result.scalars().first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.post("/vehicles/")
async def create_vehicles(
    request_model: TuroSearchRequestModel,
    db: AsyncSession = Depends(get_db)
):
    vehicles_to_add = []
    batch_vehicle_ids = set()
    vehicle_data_list = []

    try:
        # Step 1: Collect all vehicle IDs and vehicle data
        for entry in request_model.entries:
            vehicles = entry.response_content.vehicles
            for vehicle in vehicles:
                batch_vehicle_ids.add(vehicle.id)
                vehicle_data_list.append(vehicle)

        # Step 2: Query existing vehicle IDs from the database
        existing_vehicle_ids = set()
        if batch_vehicle_ids:
            stmt = select(Vehicle.id).where(Vehicle.id.in_(batch_vehicle_ids))
            result = await db.execute(stmt)
            existing_vehicle_ids = set(row[0] for row in result.fetchall())
    
        # Step 3: Prepare vehicles to add, skipping existing ones
        for vehicle in vehicle_data_list:
            if vehicle.id in existing_vehicle_ids:
                continue  # Skip vehicles that already exist

            db_vehicle = Vehicle(
                id=vehicle.id,
                car_make=vehicle.make,
                car_model=vehicle.model,
                car_type=vehicle.type,
                car_category=vehicle.seoCategory,
                car_year=vehicle.year,
                
                host_id=vehicle.hostId,

                location_city=vehicle.location.city,
                location_state=vehicle.location.state,
                location_country=vehicle.location.country,
                location_coords_lat=vehicle.location.homeLocation.lat,
                location_coords_lon=vehicle.location.homeLocation.lng,

                # record_create and record_update are automatically set by AuditableRow
            )
            vehicles_to_add.append(db_vehicle)
    
        # Add vehicles to the database
        db.add_all(vehicles_to_add)
        await db.commit()

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    
    return {"message": f"Added {len(vehicles_to_add)} vehicles to the database."}


@app.post("/booking_summaries/")
async def create_booking_summaries(
    request_model: TuroSearchRequestModel,
    db: AsyncSession = Depends(get_db)
):
    booking_summaries_to_add = []

    try:
        for entry in request_model.entries:
            vehicles = entry.response_content.vehicles
            for vehicle in vehicles:
                booking_summary = BookingSummaries(
                    vehicle_id=vehicle.id,
                    average_daily_price=vehicle.avgDailyPrice.amount,
                    currency=vehicle.avgDailyPrice.currency,
                    completed_trips=vehicle.completedTrips,
                )
                booking_summaries_to_add.append(booking_summary)

        db.add_all(booking_summaries_to_add)
        await db.commit()

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

    return {"message": f"Added {len(booking_summaries_to_add)} booking summaries to the database."}


@app.post("/booking_details")
async def create_booking_details(
    request_model: DailyPricingRequestModel,
    db: AsyncSession = Depends(get_db)
):
    booking_details_to_add = []

    try:
        vehicle_id = request_model.vehicle_id
        for daily_pricing_response in request_model.dailyPricingResponses:
            # if the car is unavailable this day then it was booked
            if daily_pricing_response.wholeDayUnavailable:
                booking_detail = BookingDetails(
                        vehicle_id = vehicle_id,
                        date = daily_pricing_response.date,
                        price = daily_pricing_response.priceWithCurrency.amount,
                        currency = daily_pricing_response.priceWithCurrency.currencyCode,
                )
                pprint(booking_detail.__dict__)
                booking_details_to_add.append(booking_detail)
            
        db.add_all(booking_details_to_add)
        await db.commit()

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    
    return {"message": f"Added {len(booking_details_to_add)} booking details to the database."}


if __name__ == "__main__":
    import uvicorn
    # uvicorn.run("main:app", host="0.0.0.0", port=8000, workers=4)
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, workers=4)
