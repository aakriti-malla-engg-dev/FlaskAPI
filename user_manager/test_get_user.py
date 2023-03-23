import requests

URL = "http://localhost:5000/users"


def test_get_user():
    mobile_no = '/9696950090'
    response = requests.get(URL + mobile_no)
    data = response.json()
    assert data['data'] == {
        "_id": "6411a88ca6c2c994c0921ba3",
        "city": "Bengaluru",
        "mobile_no": "9696950090",
        "name": "Chinki"
    }
    assert data['status'] == 200
    assert data['message'] == 'User Found!'


def test_get_user_not_found():
    mobile_no = '/9898984598'
    response = requests.get(URL + mobile_no)
    data = response.json()
    assert data['status'] == 404
    assert data['message'] == 'User not found!'


