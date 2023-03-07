from pymongo import MongoClient
from flask import Flask, jsonify, request
import json
from bson.json_util import dumps

from bson import json_util, ObjectId
from user_func import Userschema, User
from UserClass import UserSchema, UserDetails

conn = 'mongodb://127.0.0.1:27017/Users'
client = MongoClient(conn)
db = client['Users']
collection_name = db["users"]

app = Flask(__name__)


@app.route('/')
def menu():
    return """============ Menu ============ 
             <br>Add - /users [POST]
             <br>Display a User - /users/<mobile_no> [GET]
             <br>Display all Users - /users [GET]
             <br>Update User - /users/<mobile_no> [PUT]
             <br>Delete User - /users/<mobile_no> [DELETE]
             <br>=============================="""


@app.route('/users', methods=['POST'])
def add_user_to_db():
    data = json.loads(request.data)
    inserted = []
    existing = []
    user_id = data['id']
    user_name = data['name']
    mobile_no = data['mobile_no']
    city = data['city']
    if id and user_name and mobile_no and city:
        if collection_name.find_one({"mobile_no": data['mobile_no']}):
            existing.append(str(data['mobile_no']))
        else:
            status = collection_name.insert_one({
                "id": user_id,
                "name": user_name,
                "mobile_no": mobile_no,
                "city": city
            })
            inserted.append(str(data['mobile_no']))

        result = f"Inserted users: {', '.join(inserted)}\nExisting users: {', '.join(existing)}"
        return result


@app.route('/users/<mobile_no>', methods=['GET'])
def get_user_from_db(mobile_no):
    user = collection_name.find_one({'mobile_no': mobile_no})
    if user:
        result = ''
        for key, val in user.items():
            result += "{} : {}<br>".format(key, val)
        return result
    else:
        return 'User Not Found!'


@app.route('/users', methods=['GET'])
def get_users_from_db():
    users = []
    for doc in collection_name.find():
        users.append(json_util.dumps(doc))

    output = []
    for my_dict in users:
        dict_obj = json.loads(my_dict)
        for key, value in dict_obj.items():
            output.append(f"{key}: {value}")
        output.append('')

    return "<br>".join(output)


@app.route('/users/<mobile_no>', methods=['PUT'])
def update_user_in_db(mobile_no):
    updated_details = request.get_json()
    user = collection_name.find_one({'mobile_no': mobile_no})
    if user:
        collection_name.update_one({"mobile_no": mobile_no}, {"$set": updated_details})
        return dumps({'Message': 'SUCCESS'})
    else:
        return dumps({'Message': 'User not Found!'})


@app.route('/users/<mobile_no>', methods=['DELETE'])
def delete_users_from_db(mobile_no):
    deleted = collection_name.delete_one({'mobile_no': mobile_no})
    if deleted.deleted_count == 1:
        return 'User Deleted!'
    else:
        return 'User not Found!'


if __name__ == '__main__':
    app.run()
