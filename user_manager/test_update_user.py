import requests

URL = "http://localhost:5000/users"


def test_update_user():
    user_data = {
        'name': 'Diana'
    }
    mobile_no = '/7989797979'
    response = requests.put(URL + mobile_no, json=user_data)
    print(response.text)
    data = response.json()
    assert data['status'] == 200
    assert data['message'] == 'SUCCESS'


def test_update_user_not_found():
    user_data = {
        'name': 'Diana'
    }
    mobile_no = '/7569797979'
    response = requests.put(URL + mobile_no, json=user_data)
    data = response.json()
    assert data['status'] == 404
    assert data['message'] == 'User Not Found!'


def test_update_user_incorrect_name():
    user_data = {
        'name': ' Diana '
    }
    mobile_no = '/7989797979'
    response = requests.put(URL + mobile_no, json=user_data)
    data = response.json()
    assert data['status'] == 400
    assert data['message'] == 'Invalid Name!'


def test_update_user_name_len_more_than_15():
    user_data = {
        'name': 'Diana vivians solaris'
    }
    mobile_no = '/7989797979'
    response = requests.put(URL + mobile_no, json=user_data)
    data = response.json()
    assert data['status'] == 400
    assert data['message'] == 'The name\'s length should not be more than 15'


def test_update_user_wrong_city():
    user_data = {
        'city': 'Pune'
    }
    mobile_no = '/7989797979'
    response = requests.put(URL + mobile_no, json=user_data)
    data = response.json()
    assert data['status'] == 400
    assert data['message'] == 'The city must be from the following list: Delhi, Bengaluru, Kolkata, Mumbai'


def test_update_user_wrong_mobile_no_format():
    user_data = {
        'mobile_no': 2398989898
    }
    mobile_no = '/7989797979'
    response = requests.put(URL + mobile_no, json=user_data)
    data = response.json()
    assert data['status'] == 400
    assert data['message'] == 'Invalid Mobile Number'


def test_update_user_with_mobile_matching_with_other():
    user_data = {
        'mobile_no': 9090909090
    }
    mobile_no = '/7989797979'
    response = requests.put(URL + mobile_no, json=user_data)
    data = response.json()
    assert data['status'] == 400
    assert data['message'] == 'This mobile number is already registered by another user!'


def test_update_user_incorrect_mobile_length():
    user_data = {
        'mobile_no': 939898989810
    }
    mobile_no = '/7989797979'
    response = requests.put(URL + mobile_no, json=user_data)
    data = response.json()
    assert data['status'] == 400
    assert data['message'] == 'Invalid Mobile Number'

# 👉🏻 def test_update_user_passing_mobile_as_string():
#     user_data = {
#         'mobile_no': '9398989898'
#     }
#     mobile_no = '/7989797979'
#     response = requests.put(URL + mobile_no, json=user_data)
#     data = response.json()
#     assert data['status'] == 400
#     assert data['message'] == 'Invalid Mobile Number'
