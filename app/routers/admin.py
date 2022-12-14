from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from ..crud.constants import find_all_constants, update_constants
from ..database.mongo import db
from ..schemas.pricing import ConstantsBase

router = APIRouter(
    prefix="/admin",
    tags=['Pricing Parameters']
)


@router.get("")
def get_constants():
    """
    Get A list of all constants
    """
    try:
        found = find_all_constants(db)
        if not found:
            raise Exception("Constants Not Found")
        else:
            return found
    except Exception as err:
        raise HTTPException(detail={
                    'message': f"Error Al Leer Constantes {err}"
                }, status_code=400)


@router.put("")
def update_constants_values(new_constants: ConstantsBase):
    """
    Update the prices of constants
    """
    try:
        updated = update_constants(db, jsonable_encoder(new_constants))
        if not updated:
            raise Exception("Constants Not Found")
        else:
            return updated
    except Exception as err:
        raise HTTPException(detail={
                    'message': f"Error Al Actualizar Constantes {err}"
                }, status_code=400)
