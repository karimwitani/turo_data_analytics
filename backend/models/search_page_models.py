from typing import Any, List, Optional
from pydantic import BaseModel
from datetime import datetime

class TuroSearchRequestModel(BaseModel):
    data_type: str
    timestamp: datetime
    entries: List['Entry']


class Entry(BaseModel):
    request_method: str
    request_url: str
    response_status: int
    response_status_text: Optional[str]
    response_content: 'ResponseContent'


class ResponseContent(BaseModel):
    banner: 'Banner'
    dismissibleBanner: Optional[Any]
    makesFilterCount: Optional[Any]
    searchId: str
    searchLocation: 'SearchLocation'
    totalHits: int
    vehicles: List['VehicleSearchModel']


class Banner(BaseModel):
    actionText: Optional[str]
    bannerDesign: 'BannerDesign'
    bannerName: str
    text: str
    title: Optional[str]


class SearchLocation(BaseModel):
    appliedRadius: 'AppliedRadius'
    country: str
    isOperational: bool
    locationId: Optional[Any]
    name: Optional[Any]
    point: 'Point'
    shortName: Optional[Any]
    topPois: List[Any]
    type: str


class AppliedRadius(BaseModel):
    unit: str
    value: float


class Point(BaseModel):
    lat: float
    lng: float


class BannerDesign(BaseModel):
    animationLoopCount: Optional[int]
    animationURL: Optional[str]
    clickableURL: Optional[str]
    designVariant: Optional[str]
    resizeableIconDarkURL: str
    resizeableIconURL: str
    withBorder: bool


class AvgDailyPrice(BaseModel):
    amount: float
    currency: str

class Image(BaseModel):
    originalImageUrl: str
    resizeableUrlTemplate: str


class HomeLocation(BaseModel):
    lat: float
    lng: float


class Distance(BaseModel):
    unit: str
    value: float


class LocationSlugs(BaseModel):
    fr_CA: str
    en_GB: str
    en_CA: str
    en_US: str
    en_AU: str
    fr_FR: str


class Location(BaseModel):
    city: str
    country: str
    distance: Distance
    homeLocation: HomeLocation
    isDelivery: bool
    locationId: Optional[Any]  # Adjust type if more information is available
    locationSlugs: LocationSlugs
    state: str


class Tag(BaseModel):
    label: str
    type: str


class VehicleSearchModel(BaseModel):
    availability: Optional[Any]  
    avgDailyPrice: AvgDailyPrice
    completedTrips: int
    estimatedQuote: Optional[Any]  
    hostId: int
    id: int
    images: List[Image]
    isAllStarHost: bool
    isFavoritedBySearcher: bool
    isNewListing: bool
    location: Location
    make: str
    model: str
    rating: float
    seoCategory: str
    tags: List[Tag]
    type: str
    year: int