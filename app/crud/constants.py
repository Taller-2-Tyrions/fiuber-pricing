from pymongo import ReturnDocument

CONSTANTS_NAME = "CONSTANTS"


def find_all_constants(db):
    found = db["pricing"].find_one({"name": CONSTANTS_NAME}, {"_id": 0})

    return found.get("values")


def update_constants(db, changes):
    finder = {"name": CONSTANTS_NAME}
    after = ReturnDocument.AFTER
    changes = {"values": changes}
    found = db["pricing"].find_one_and_update(finder, {"$set": changes},
                                              return_document=after)

    return found.get("values")
