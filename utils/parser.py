import json
from requests import Response
from typing import Dict, Any


def get_response_as_dict(response: Response) -> Dict[str, Any]:
    """Converting a JSON response to a dictionary"""
    try:
        return response.json()
    except json.JSONDecodeError:
        assert False, \
            f"Response is not JSON format. Response text is '{response.text}'"
