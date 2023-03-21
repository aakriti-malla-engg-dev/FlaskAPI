import requests

URL = "http://localhost:5000/users"


def test_delete_user_with_yes_param():
    mobile_no = '/7989797979'
    response = requests.delete(URL+mobile_no+'?confirm=YES')
    data = response.json()
    assert data['status'] == 204
    assert data['message'] == 'User Deleted!'


def test_delete_user_without_param():
    mobile_no = '/9191919191'
    response = requests.delete(URL + mobile_no)
    data = response.json()
    assert data['status'] == 204
    assert data['message'] == 'Give Confirmation in order to delete!'


def test_delete_user_not_found():
    mobile_no = '/7985997979'
    response = requests.delete(URL + mobile_no)
    data = response.json()
    assert data['status'] == 404
    assert data['message'] == 'User Not Found!'
