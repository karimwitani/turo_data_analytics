from pydantic import BaseModel
from typing import List
from datetime import date

class PriceWithCurrency(BaseModel):
    amount: float
    currencyCode: str

class DailyPricingResponse(BaseModel):
    custom: bool
    date: date
    localizedDayOfWeek: str
    localizedShortDayOfWeek: str
    price: float
    priceEditable: bool
    priceWithCurrency: PriceWithCurrency
    source: str
    wholeDayUnavailable: bool

class DailyPricingRequestModel(BaseModel):
    vehicle_id: int
    calendarCurrencyHeader: str
    dailyPricingResponses: List[DailyPricingResponse]
