




from database import db
from bson.objectid import ObjectId

def create_item(data):
    result = db.items.insert_one(data)
    return str(result.inserted_id)

def get_all_items():
    items = db.items.find()
    result = []
    
    for item in items:
        print(item)
        item['id'] = str(item.pop("_id"))
        print(item)
        result.append(item)
    
    return result
    

def get_item(item_id):
    item = db.items.find_one({"_id": ObjectId(item_id)})
    
    if item:
        item["id"] = str(item.pop("_id"))
    return item


def update_item(item_id, data):
    result = db.items.update_one({"_id": ObjectId(item_id)}, {"$set":data})
    # return get_item(item_id)
    return result


def delete_item(item_id):
    result = db.items.delete_one({"_id": ObjectId(item_id)})
    return result.deleted_count