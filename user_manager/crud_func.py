import bson
import pymongo
from pymongo import MongoClient
from flask import Flask, jsonify, request
import json
from bson.json_util import dumps

from bson import json_util, ObjectId

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
    try:
        data = request.json
        user_name = data['name']
        mobile_no = data['mobile_no']
        city = data['city']
        if user_name and mobile_no and city:
            if collection_name.find_one({"mobile_no": data['mobile_no']}):
                user = collection_name.find_one({"mobile_no": data['mobile_no']})
                user_id = str(user['_id'])
                return jsonify({
                    "status": 200,
                    "message": "User Already Exists!",
                    "id": user_id
                })
            else:
                status = collection_name.insert_one({
                    "name": user_name,
                    "mobile_no": mobile_no,
                    "city": city
                })
                user_id = str(status.inserted_id)
                return jsonify({
                    "status": 201,
                    "message": "User Created!",
                    "data": {
                        "id": user_id
                    }
                })
        else:
            return jsonify({
                "status": 400,
                "message": "Invalid Request Data"
            })
    except Exception as e:
        return jsonify({
            'Error': str(e),
            'status': 404
        })


@app.route('/users/<mobile_no>', methods=['GET'])
def get_user_from_db(mobile_no):
    try:
        user = collection_name.find_one({'mobile_no': mobile_no})
        if user:
            result = {}
            for key, val in user.items():
                if isinstance(val, ObjectId):
                    result[key] = str(val)
                else:
                    result[key] = val
            return jsonify({
                "status": 200,
                'data': result,
                'message': 'User Found!'
            })
        else:
            return jsonify({
                'status': 404,
                'message': 'User not found!'
            })
    except pymongo.errors.ConnectionFailure:
        print("Connection Error!")
    except pymongo.errors.OperationFailure as e:
        print(f"MongoDB operation failed with error: {e}")
    except Exception as e:
        return jsonify({
            'status': 500,
            'Message': 'Internal Server Error: ' + str(e)
        })


@app.route('/users', methods=['GET'])
def get_users_from_db():
    try:
        users = []
        for doc in collection_name.find():
            users.append(json_util.dumps(doc))

        output = []
        for my_dict in users:
            dict_obj = json.loads(my_dict)
            output.append(dict_obj)

        return jsonify({
            "status": 200,
            "data": output,
            "message": "Users Found!"
        })
    except pymongo.errors.ConnectionFailure:
        print("Connection Error!")
    except pymongo.errors.OperationFailure as e:
        print(f"MongoDB operation failed with error: {e}")
    except Exception as e:
        return jsonify({
            'status': 500,
            'Message': 'Internal Server Error: ' + str(e)
        })


@app.route('/users/<mobile_no>', methods=['PUT'])
def update_user_in_db(mobile_no):
    updated_details = request.get_json()
    user = collection_name.find_one({'mobile_no': mobile_no})
    try:
        if user:
            collection_name.update_one({"mobile_no": mobile_no}, {"$set": updated_details})
            return jsonify({
                'Message': 'SUCCESS',
                'status': 200
            })
        else:
            return jsonify({
                'status': 404,
                'Message': 'User Not Found!'
            })
    except pymongo.errors.ConnectionFailure:
        print("Connection Error!")
    except pymongo.errors.OperationFailure as e:
        print(f"MongoDB operation failed with error: {e}")
    except Exception as e:
        return jsonify({
            'status': 500,
            'Message': 'Internal Server Error: ' + str(e)
        })


@app.route('/users/<int:mobile_no>', methods=['DELETE'])
def delete_users_from_db(mobile_no):
    try:
        deleted = collection_name.delete_one({'mobile_no': mobile_no})
        if deleted.deleted_count == 1:
            return jsonify({
                'status': 204,
                'message': 'User Deleted!'
            })

        else:
            return jsonify({
                'status': 404,
                'message': 'User Not Found!'
            })
    except pymongo.errors.ConnectionFailure:
        print("Connection Error!")
    except pymongo.errors.OperationFailure as e:
        print(f"MongoDB operation failed with error: {e}")
    except Exception as e:
        return jsonify({
            'status': 500,
            'message': 'Error deleting user',
            'error': str(e)
        })


if __name__ == '__main__':
    app.run()
