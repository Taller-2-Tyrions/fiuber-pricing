import mongomock
from app.crud import constants as cst


def add_all_constants(db, constants):
    db["pricing"].insert_one({"name": cst.CONSTANTS_NAME, "values": constants})


def test_create_user():
    db = mongomock.MongoClient().db
    constants = {"CONSTANTE_1": 10,
                 "CONSTANTE_2": 20}
    add_all_constants(db, constants)
    all_constants = cst.find_all_constants(db)
    
    assert (all_constants == constants)


def test_changes_accepted():
    db = mongomock.MongoClient().db
    constants = {"CONSTANTE_1": 10,
                 "CONSTANTE_2": 20}
    add_all_constants(db, constants)
    changes = {"CONSTANTE_1": 15,
               "CONSTANTE_2": 29}
    all_constants = cst.update_constants(db, changes)

    assert (all_constants == changes)
