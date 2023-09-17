import allure
import json
from requests import Response
from pydantic import ValidationError
from typing import Dict, Any


class Asserts:

    @staticmethod
    @allure.step("Response status code: {expected_status_code}")
    def status_code_should_be(response: Response, expected_status_code: int) -> None:
        """Check the current status code of the response for compliance with the expected status code"""
        actual_status_code = response.status_code
        assert expected_status_code == actual_status_code, \
            f"\nUnexpected status code! Expected: {expected_status_code}. Actual: {actual_status_code}"

    @staticmethod
    @allure.step("JSON response schema is valid")
    def validate_response(response: Response, schema) -> None:
        """Check the received response for compliance with the JSON schema"""
        response_json = Asserts._get_response_as_dict(response)
        try:
            schema.model_validate(response_json)
        except ValidationError as e:
            raise AssertionError(f"JSON schema validation failed: {e}")

    def _get_response_as_dict(response: Response) -> Dict[str, Any]:
        """Converting a JSON response to a dictionary"""
        try:
            return response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not JSON format. Response text is '{response.text}'"