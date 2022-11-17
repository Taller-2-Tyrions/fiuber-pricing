from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from ..services.pricing import price_voyage, add_vip_price
from ..schemas.pricing import PriceRequestBase, PriceRequestsBase


router = APIRouter(
    prefix="/pricing",
    tags=['Calculate Prices']
)


@router.post("/voyage")
def get_voyage_info(request: PriceRequestBase):
    try:
        price = price_voyage(request.voyage, request.driver, request.passenger)
        print("Calculado")
        if request.voyage.is_vip:
            price = add_vip_price(price)
    except Exception as err:
        raise HTTPException(detail={
                    'message': f"Error Al Cotizar {err}"
                }, status_code=400)

    return price


@router.post("/voyages")
def get_voyages_info(request: PriceRequestsBase):
    prices = {}
    try:
        for driver in request.drivers:
            price = price_voyage(request.voyage, driver, request.passenger)
            id = driver.id
            if request.voyage.is_vip:
                price = add_vip_price(price)
            prices.update({id: price})
    except Exception as err:
        raise HTTPException(detail={
                    'message': f"Error Al Cotizar {err}"
                }, status_code=400)

    return prices
