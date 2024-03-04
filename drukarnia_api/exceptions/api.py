from __future__ import annotations


class DrukarniaAPIError(Exception):
    def __init__(self, message: str, status_code: int | str, request_type: str, request_url: str) -> None:
        self.message = message
        self.status_code = status_code
        self.request_type = request_type
        self.request_url = request_url

    def __str__(self) -> str:
        return f"""
        Request Type: {self.request_type}
        Response Status: {self.status_code}
        Request To: {self.request_url}
        Error Message: "{self.message}"
        """

