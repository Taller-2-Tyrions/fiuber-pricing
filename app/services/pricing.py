
import requests
import os
from fastapi.exceptions import HTTPException

from datetime import datetime, time

from ..schemas.pricing import VoyageBase, DriverBase
from ..database.mongo import db

from ..crud.constants import find_all_constants

PRICE_PER_METER = 1.5
PRICE_PER_MINUTE = 1.5
PRICE_PER_VIP = 1.2
NIGHT_PLUS = 1.2
DISCOUNT_SENIORITY_DRIVER = 1
DISCOUNT_DAILY_DRIVER = 1
DISCOUNT_MONTHLY_DRIVER = 1
DISCOUNT_SENIORITY_CLIENT = 1
DISCOUNT_DAILY_CLIENT = 1
DISCOUNT_MONTHLY_CLIENT = 1
PRICE_WAIT_CONF = 1
PRICE_ARRIVAL = 1

BASE_PRICE_CLIENT = 50
MAX_DISCOUNT_DRIVER = 50

NIGHT_START = time(20, 0)
NIGHT_END = time(6, 0)

AVERAGE_DRIVER_PRICE = 10
AVERAGE_TIME_AWAIT = 10

GOOGLE_MAPS_URL = os.getenv("GOOGLE_MAPS_URL")
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")


def is_status_correct(status_code):
    return status_code//100 == 2


def distance_to(_origin_point, _dest_point):
    origin_point = str(_origin_point.latitude)+','+str(_origin_point.longitude)
    dest_point = str(_dest_point.latitude)+','+str(_dest_point.longitude)

    resp = requests.get(GOOGLE_MAPS_URL+"?origins=" + origin_point +
                        "&destinations=" + dest_point +
                        "&unit=km&key=" + GOOGLE_MAPS_API_KEY)
    if (not is_status_correct(resp.status_code)):
        print("Error in Google Maps Services: pricing::distance_to")
        raise HTTPException(detail={
                    'message': resp.reason
                }, status_code=500)

    resp_json = resp.json()
    distance_in_mts = resp_json['rows'][0]['elements'][0]['distance']['value']

    return distance_in_mts


def time_to(point_a, point_b):
    return distance_to(point_a, point_b)*0.1


def get_price_driver(driver: DriverBase, constants):
    total_price = driver.day_voyages * constants.get("daily_driver")
    total_price += driver.month_voyages * constants.get("monthly_driver")
    total_price += driver.seniority * constants.get("seniority_driver")

    if total_price > constants.get("max_increase_driver"):
        total_price = constants.get("max_increase_driver")

    return total_price


def get_price_client(pasenger, constants):
    total_price = constants.get("max_discount_passenger")
    total_price -= pasenger.day_voyages * constants.get("daily_passenger")
    total_price -= pasenger.month_voyages * constants.get("monthly_passenger")
    total_price -= pasenger.seniority * constants.get("seniority_passenger")

    if total_price < 0:
        total_price = 0

    return total_price


def is_night():
    now = datetime.utcnow()
    now_time = now.time()

    if now_time >= NIGHT_START or now_time <= NIGHT_END:
        return True

    return False


def get_price_voyage(voyage: VoyageBase, constants):
    price = distance_to(voyage.init, voyage.end) * constants.get("price_meter")
    price += time_to(voyage.init, voyage.end) * constants.get("price_minute")

    return price


def get_time_await(driver, init, constants):
    location = driver.get("location")
    price = time_to(location, init) * constants.get("price_minute")
    price += distance_to(location, init) * constants.get("price_meter")

    return price


def price_voyage(voyage: VoyageBase, driver: DriverBase):
    constants = find_all_constants(db)
    price_voyage = get_price_voyage(voyage, constants)
    price_driver = get_price_driver(driver, constants)
    price_client = get_price_client(voyage.passenger)
    price_time_await = get_time_await(driver, voyage.init, constants)

    total_price = price_voyage + price_driver + price_client + price_time_await

    if is_night():
        total_price *= constants.get("plus_night")

    return total_price


def add_vip_price(price):
    constants = find_all_constants(db)
    return price * constants.get("price_vip")
