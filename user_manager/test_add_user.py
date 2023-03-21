import json
import requests
import pymongo
from bson import ObjectId, json_util

from UserManager import collection_name

URL = "http://localhost:5000/users"


def test_add_user():
    user_data = {
        'name': 'Happy Kia',
        'mobile_no': '9656565652',
        'city': 'Bengaluru'
    }

    response = requests.post(URL, json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 200
    assert data['message'] == "User Created!"


def test_add_user_already_exist():
    user_data = {
        'name': 'Pia',
        'mobile_no': '9079890192',
        'city': 'Delhi'
    }
    response = requests.post(URL, json=user_data)
    assert response.status_code == 200

    data = response.json()
    assert data['status'] == 200
    assert data['message'] == 'User Already Exists!'
    assert 'id' in data
    assert str(collection_name.find_one({'mobile_no': '9079890192'})['_id']) == data['id']


def test_add_user_name_with_space_at_beg_and_end():
    user_data = {
        'name': ' Chia ',
        'mobile_no': '7989797979',
        'city': 'Delhi'
    }
    response = requests.post(URL, json=user_data)
    data = response.json()
    assert data['status'] == 400
    assert data['message'] == 'Invalid Name!'


def test_add_user_name_with_length_more_than_15_char():
    user_data = {
        'name': 'Lilly solaris vivians',
        'mobile_no': '9079890192',
        'city': 'Delhi'
    }
    response = requests.post(URL, json=user_data)
    data = response.json()
    assert data['status'] == 400
    assert data['message'] == 'Name length more than 15 characters!'


def test_add_user_empty_name():
    user_data = {
        'name': '',
        'mobile_no': '9079890192',
        'city': 'Delhi'
    }
    response = requests.post(URL, json=user_data)
    data = response.json()
    assert data['status'] == 400
    assert data['message'] == 'Invalid Name!'


def test_add_user_invalid_name():
    user_data = {
        'name': 'samy10',
        'mobile_no': '9079890192',
        'city': 'Delhi'
    }
    response = requests.post(URL, json=user_data)
    data = response.json()
    assert data['status'] == 400
    assert data['message'] == 'Invalid Name!'


def test_add_user_with_invalid_mobile_no():
    user_data = {
        'name': 'Chia',
        'mobile_no': '2989797979',
        'city': 'Delhi'
    }
    response = requests.post(URL, json=user_data)
    data = response.json()
    assert data['status'] == 400
    assert data['message'] == 'Invalid Mobile format or it should be of 10 digits!'


def test_add_user_with_invalid_length_mobile_no():
    user_data = {
        'name': 'Chia',
        'mobile_no': '79897979790',
        'city': 'Delhi'
    }
    response = requests.post(URL, json=user_data)
    data = response.json()
    assert data['status'] == 400
    assert data['message'] == 'Invalid Mobile format or it should be of 10 digits!'


def test_add_user_wrong_city():
    user_data = {
        'name': 'Diana',
        'mobile_no': '9989797979',
        'city': 'Pune'
    }
    response = requests.post(URL, json=user_data)
    data = response.json()
    assert data['status'] == 400
    assert data['message'] == 'The city must be from the following list: Delhi, Bengaluru, Kolkata, Mumbai'


def test_add_user_missing_field():
    user_data = {
        'city': 'Delhi'
    }
    response = requests.post(URL, json=user_data)
    data = response.json()
    assert data['status'] == 404
    assert data['message'] == ['name is not present', 'mobile_no is not present']


def test_add_user_invalid_request():
    user_data = {
        'name': 'Diana',
        'mobile_no': '9989797979',
        'city': 'Delhi',
        'so': 'check'
    }
    response = requests.post(URL, json=user_data)
    data = response.json()
    assert data['status'] == 400
    assert data['message'] == 'Invalid field(s): so'


