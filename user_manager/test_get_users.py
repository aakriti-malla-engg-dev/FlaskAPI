import pymongo
import requests
import json
from UserManager import get_users_from_db, app

URL = "http://localhost:5000/users"


def test_get_users():
    response = requests.get(URL)
    assert response.status_code == 200
    data = response.json()
    assert len(data['data']) > 0


def test_get_users_failure():
    response = requests.get(URL)
    assert response.status_code == 200
    data = response.json()
    assert len(data['data']) == 0

