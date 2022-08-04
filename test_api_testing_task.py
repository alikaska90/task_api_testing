import pytest
from queries import APIQueriesHelper as Queries


@pytest.fixture(scope='module')
def user_registration_for_tests():
    registration_data = {
        'email': 'eve.holt@reqres.in',
        'password': 'pistol'
    }
    queries = Queries()
    registration_response = queries.user_registration(user_data=registration_data)
    return registration_response


test_parameters = [
    ('eve.holt@reqres.in', 'pistol', True),
    ('eve.holt@reqres', 'pistol', False),
    ('eve.holt@reqres.in', '', False)
]


@pytest.mark.parametrize('email, password, correct', test_parameters)
def test_check_registration_and_login(user_registration_for_tests, email, password, correct):
    registration_response = user_registration_for_tests
    # check that user was registered
    assert registration_response["code"] == 200, "User wasn't registered"
    # check that response has token
    assert "token" in registration_response["body"]
    user_token = registration_response["body"]["token"]

    # login request
    queries = Queries()
    user_data = {"email": email, "password": password}
    login_response = queries.login(user_data=user_data)
    if correct:
        # check status code for successful login
        assert login_response["code"] == 200, f"User wasn't logged in, error: {login_response['body']['error']}"
        # check token
        assert user_token == login_response['body']['token']
    else:
        assert login_response["code"] == 400, "Incorrect status cod for unsuccessful login"


def test_check_user_list():
    existing_user = {
        "id": 7,
        "email": "michael.lawson@reqres.in",
        "first_name": "Michael",
        "last_name": "Lawson",
        "avatar": "https://reqres.in/img/faces/7-image.jpg"
    }
    queries = Queries()
    user_list_response = queries.get_user_list(page=2)
    assert user_list_response["code"] == 200, "User list wasn't received"
    # check that user list is in response
    assert "data" in user_list_response["body"], "There is no user list in response"
    # check that user is in the list
    user_list = user_list_response["body"]["data"]
    user_by_id = [user for user in user_list if user["id"] == existing_user["id"]]
    assert len(user_by_id) == 1, f"There are several users with id = {existing_user['id']}"
    assert user_by_id, f"User with id = {existing_user['id']} wasn't found"
    # check user fields
    assert existing_user == user_by_id[0], "Fields for user in response are incorrect"


user_creation_data = [("morpheus", "leader")]


@pytest.mark.parametrize("name, job", user_creation_data)
def test_user_creation_and_modifying(name, job):
    queries = Queries()
    user_creation_response = queries.create_user(user_data={"name": name, "job": job})
    assert user_creation_response["code"] == 201, "User wasn't created"
    response_time = user_creation_response["response_time"]
    print("Response time in seconds: ", response_time)
    user_id = user_creation_response["body"]["id"]
    new_job = "zion resident"
    updated_user_data = {"name": name, "job": new_job}
    user_modifying_response = queries.update_user(user_id=user_id, user_data=updated_user_data)
    assert user_modifying_response["code"] == 200, f"User with id = {user_id} wasn't modified"
    response_body = user_modifying_response["body"]
    assert "updatedAt" in response_body, "There is no date of updating in response"
    data_from_response = {key: response_body[key] for key in response_body if key in ["name", "job"]}
    assert updated_user_data == data_from_response, "Data in response is incorrect"
