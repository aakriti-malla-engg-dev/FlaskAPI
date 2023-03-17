import pytest
from pytest_steps import test_steps
from jsonschema import validate
from UserManager import get_users_from_db, delete_users_from_db, update_user_in_db, add_user_to_db, get_user_from_db


class UserManger:

    @test_steps(
        'test_get_user'
    )
    def test_get_user(self):
        user_data = get_user_from_db
