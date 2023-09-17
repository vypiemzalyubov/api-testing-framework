import allure
from pydantic import ValidationError
from utils.parser import get_response_as_dict


class Asserts:

    def __init__(self, response) -> None:
        self.response = response

    @allure.step("Response status code: {expected_status_code}")
    def status_code_should_be(self, expected_status_code: int) -> 'Asserts':
        """Check the current status code of the response for compliance with the expected status code"""
        actual_status_code = self.response.status_code
        assert expected_status_code == actual_status_code, \
            f"Unexpected status code! Expected: {expected_status_code}. Actual: {actual_status_code}"
        return self

    @allure.step("JSON response schema is valid")
    def validate_response(self, schema) -> 'Asserts':
        """Check the received response for compliance with the JSON schema"""
        response_json = get_response_as_dict(self.response)
        try:
            schema.model_validate(response_json)
        except ValidationError as e:
            raise AssertionError(f"JSON schema validation failed: {e}")
        return self
