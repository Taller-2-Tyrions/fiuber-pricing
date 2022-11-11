from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from ..services.pricing import price_voyage, add_vip_price
from ..schemas.pricing import VoyageBase, DriverBase

from typing import List


router = APIRouter(
    prefix="/pricing",
    tags=['Calculate Prices']
)


@router.post("/voyage/")
def get_voyage_info(voyage: VoyageBase, driver: DriverBase,
                    is_vip: bool):
    try:
        price = price_voyage(voyage, driver)
        print("Calculado")
        if is_vip:
            price = add_vip_price(price)
    except Exception as err:
        raise HTTPException(detail={
                    'message': f"Error Al Cotizar {err}"
                }, status_code=400)

    return price


@router.post("/voyages/")
def get_voyages_info(voyage: VoyageBase, near_drivers: List[DriverBase],
                     is_vip: bool):
    prices = {}
    try:
        for driver in near_drivers:
            price = price_voyage(voyage, driver)
            id = driver.id
            if is_vip:
                price = add_vip_price(price)
            prices.update({id: price})
    except Exception as err:
        raise HTTPException(detail={
                    'message': f"Error Al Cotizar {err}"
                }, status_code=400)

    return prices
