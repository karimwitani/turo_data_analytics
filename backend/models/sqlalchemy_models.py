import datetime

from sqlalchemy import Column, Integer, Boolean, String, DateTime, Float, ForeignKey, event
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    is_offer = Column(Boolean, default=False)


class AuditableRow():
    record_create = Column(DateTime)
    record_update = Column(DateTime)

# The below two events drive automatic timestamp creation/update for all subclasses of AuditableRow
@event.listens_for(AuditableRow, 'before_insert', propagate=True)
def set_created_at(mapper, connection, target):
    now = datetime.datetime.now(datetime.timezone.utc)
    target.record_create = now
    target.record_update = now

@event.listens_for(AuditableRow, 'before_update', propagate=True)
def set_updated_at(mapper, connection, target):
    target.record_update = datetime.datetime.now(datetime.timezone.utc)


class Vehicle(Base, AuditableRow):
    __tablename__= 'vehicles'
    
    id = Column(Integer,  primary_key=True, index=True)
    car_make = Column(String)
    car_model = Column(String)
    car_type = Column(String)
    car_category = Column(String)
    car_year = Column(Integer)
    
    host_id = Column(Integer)

    location_city = Column(String)
    location_state = Column(String)
    location_country = Column(String)
    location_coords_lat = Column(Float)
    location_coords_lon = Column(Float)


    # Establish relationship with BookingSummaries
    booking_summaries = relationship(
        "BookingSummaries",
        back_populates="vehicle",
        cascade="all, delete-orphan"
    )

class BookingSummaries(Base, AuditableRow):
    __tablename__= 'booking_summaries'
    id = Column(Integer, primary_key=True)
    vehicle_id = Column(Integer, ForeignKey('vehicles.id'), nullable=False)
    
    average_daily_price = Column(Float)
    currency = Column(String)
    completed_trips = Column(Integer)

    # Establish relationship back to Vehicle
    vehicle = relationship(
        "Vehicle",
        back_populates="booking_summaries"
    )
