class DrukarniaAPIError(Exception):
    def __init__(self, message: str, status_code: int or str, request_type: str, request_url: str):
        """
        Custom exception class for handling errors in the Drukarnia API.

        Args:
            message (str): The error message.
            status_code (int or str): The status code of the API response.
            request_type (str): The type of the API request.
            request_url (str): The URL of the API request.
        """

        self.message = message
        self.status_code = status_code
        self.request_type = request_type
        self.request_url = request_url

    def __str__(self):
        """
        Returns a string representation of the exception.
        """
        text = f"""
        Request Type: {self.request_type}
        Response Status: {self.status_code}
        Request To: {self.request_url}
        Error Message: "{self.message}"
        """

        return text
