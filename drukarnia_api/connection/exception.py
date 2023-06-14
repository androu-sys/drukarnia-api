class DrukarniaException(Exception):
    def __init__(self, message: str, status_code: int or str, request_type: str, request_url: str):

        self.message = message
        self.status_code = status_code
        self.request_type = request_type
        self.request_url = request_url

    def __str__(self):

        text = f"""
        \nRequest Type: {self.request_type}; Response Status: {self.status_code};
        \nRequest To: {self.request_url}; \nError Message: "{self.message}";
        """

        return text
