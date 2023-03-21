import re

import bson
import pymongo
from pymongo import MongoClient
from flask import Flask, jsonify, request
import json
from bson.json_util import dumps
import traceback
import sys

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
    """ Function is used to add a new user to the database. """
    try:
        data = request.json
        fields = ['name', 'mobile_no', 'city']
        cities = ['Delhi', 'Bengaluru', 'Mumbai', 'Kolkata']

        # check for missing fields
        missing_fields = []
        for field in fields:
            if field not in data:
                missing_fields.append(field + ' is not present')
        if len(missing_fields) > 0:
            return jsonify({
                'status': 404,
                'message': missing_fields
            })

        valid_fields = set(fields)

        # Check for invalid fields
        invalid_fields = set(data.keys()) - valid_fields
        if invalid_fields:
            return jsonify({
                'status': 400,
                'message': f'Invalid field(s): {", ".join(invalid_fields)}'
            })

        user_name = data['name']
        mobile_no = data['mobile_no']
        city = data['city']

        # mobile number format check
        if not re.match(r"^[6-9]\d{9}$", mobile_no):
            return jsonify({
                "status": 400,
                "message": "Invalid Mobile format or it should be of 10 digits!"
            })

        # city check
        if city not in cities:
            return jsonify({
                'status': 400,
                'message': 'The city must be from the following list: Delhi, Bengaluru, Kolkata, Mumbai'
            })

        # Name format check
        if not re.search(r'^[a-zA-Z]+(?: [a-zA-Z]+)*$', user_name):
            return jsonify({
                'status': 400,
                'message': 'Invalid Name!'
            })

        # Name length check
        if len(user_name) > 15:
            return jsonify({
                'status': 400,
                'message': 'Name length more than 15 characters!'
            })

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
                    "status": 200,
                    "message": "User Created!",
                    "data": {
                        "id": user_id
                    }
                })
        else:
            return jsonify({
                "status": 400,
                "message": "Invalid Request!"
            })
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({
            'Error': str(e),
            'status': 404
        })


@app.route('/users/<mobile_no>', methods=['GET'])
def get_user_from_db(mobile_no):
    """ Function to get user from the database. """
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
    """ Function to get all users from the database. """
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


@app.route('/users/<int:mobile_no>', methods=['PUT'])
def update_user_in_db(mobile_no):
    """ Function to update user info in the database. """
    updated_details = request.json
    cities = ['Delhi', 'Bengaluru', 'Mumbai', 'Kolkata']
    user = collection_name.find_one({'mobile_no': mobile_no})
    try:
        if user:
            if 'name' in updated_details:
                name = updated_details['name']
                if not name.isalpha() or len(name) > 15:
                    return jsonify({
                        'status': 400,
                        'message': 'Invalid Name - The name\'s length should not be more than 15 and can only contain '
                                   'alphabetical characters!'
                    })
                updated_details['name'] = name
            if 'city' in updated_details:
                city = updated_details['city']
                if city not in cities:
                    return jsonify({
                        'status': 400,
                        'message': 'The city must be from the following list: Delhi, Bengaluru, Kolkata, Mumbai'
                    })
                updated_details['city'] = city

            if 'mobile_no' in updated_details:
                new_mobile_no = updated_details['mobile_no']
                if not isinstance(mobile_no, int):
                    try:
                        new_mobile_no = int(new_mobile_no)
                    except ValueError:
                        return jsonify({
                            "status": 400,
                            "message": "Invalid Mobile Number"
                        })

                if not re.match(r"^[6-9]\d{9}$", str(new_mobile_no)):
                    return jsonify({
                        "status": 400,
                        "message": "Invalid Mobile Number"
                    })
                if collection_name.find_one({'mobile_no': new_mobile_no, 'name': {'$ne': user['name']}}):
                    return jsonify({
                        'status': 400,
                        'message': 'This mobile number is already registered by another user!'
                    })
                updated_details['mobile_no'] = mobile_no

            collection_name.update_one({"mobile_no": mobile_no}, {"$set": updated_details})
            return jsonify({
                'Message': 'SUCCESS',
                'status': 200
            })
        else:
            print(traceback.format_exc())
            return jsonify({
                'status': 404,
                'Message': 'User Not Found!'
            })
    except pymongo.errors.ConnectionFailure:
        print("Connection Error!")
    except pymongo.errors.OperationFailure as e:
        print(f"MongoDB operation failed with error: {e}")
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({
            'status': 500,
            'Message': 'Internal Server Error: ' + str(e)
        })


@app.route('/users/<int:mobile_no>', methods=['DELETE'])
def delete_users_from_db(mobile_no):
    """ Function to delete user from the database. """
    try:
        user = collection_name.find_one({'mobile_no': mobile_no})
        if user:
            confirmation = request.args.get('confirm')
            if confirmation == 'YES':
                collection_name.delete_one({'mobile_no': mobile_no})
                return jsonify({
                    'status': 204,
                    'message': 'User Deleted!'
                })
            else:
                return jsonify({
                    'status': 204,
                    'message': 'Give Confirmation in order to delete!'
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
