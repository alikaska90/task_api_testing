import requests
import json.decoder


def create_return_data(response) -> dict:
    response_code = response.status_code
    try:
        response_body = response.json()
    except json.decoder.JSONDecodeError:
        assert False, f"Response isn't in format JSON. Response text: {response.text}"
    return {"code": response_code, "body": response_body}


class APIQueriesHelper:
    def __init__(self):
        self.url = "https://reqres.in/api/"

    def user_registration(self, user_data: dict) -> dict:
        url = self.url + "register"
        registration_request = requests.post(url=url, data=user_data)
        return create_return_data(registration_request)

    def login(self, user_data: dict) -> dict:
        url = self.url + "login"
        login_request = requests.post(url=url, data=user_data)
        return create_return_data(login_request)

    def get_user_list(self, page: int) -> dict:
        url = self.url + "users"
        user_list_request = requests.get(url, params={"page": page})
        return create_return_data(user_list_request)

    def create_user(self, user_data: dict) -> dict:
        url = self.url + "users"
        user_creation_request = requests.post(url, data=user_data)
        result = create_return_data(user_creation_request)
        result["response_time"] = user_creation_request.elapsed.total_seconds()
        return result

    def update_user(self, user_id: str, user_data: dict) -> dict:
        url = self.url + "users/" + user_id
        user_modifying_request = requests.put(url, data=user_data)
        return create_return_data(user_modifying_request)
