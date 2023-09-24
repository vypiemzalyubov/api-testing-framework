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
    def validate_schema(self, schema) -> 'Asserts':
        """Check the received response for compliance with the JSON schema"""
        response_json = get_response_as_dict(self.response)
        if isinstance(response_json, list):
            for item in response_json:
                try:
                    schema.model_validate(item)
                except ValidationError as e:
                    raise AssertionError(f"JSON schema validation failed for item: {e}")
        else:
            try:
                schema.model_validate(response_json)
            except ValidationError as e:
                raise AssertionError(f"JSON schema validation failed: {e}")
        return self

    @allure.step("The response field contains the expected value")
    def have_value_in_key(self, key: str, expected_value: str) -> 'Asserts':
        """Checking the value in the specified key"""
        response_json = get_response_as_dict(self.response)
        for item in response_json["detail"]:
            assert expected_value == item[key], \
                f"Response doesn't contain the {expected_value} in the key {key}"
        return self
