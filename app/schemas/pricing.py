from pydantic import BaseModel


class Point(BaseModel):
    longitude: float
    latitude: float


class UserBase(BaseModel):
    seniority: int
    day_voyages: int
    month_voyages: int


class VoyageBase(BaseModel):
    passenger: UserBase
    init: Point
    end: Point
    is_vip: bool


class DriverBase(UserBase):
    id: str
    location: Point
    is_vip: bool


class ConstantsBase(BaseModel):
    price_meter: float
    price_minute: float
    price_vip: float
    plus_night: float
    seniority_driver: float
    daily_driver: float
    monthly_driver: float
    seniority_passenger: float
    daily_passenger: float
    monthly_passenger: float
    max_discount_passenger: float
    max_increase_driver: float
