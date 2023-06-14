class DrukarniaException(Exception):
    def __init__(self, message: str, code: int or str, request_type: str, request_url: str):

        text = """
        Request Type: {request_type}; Status Code: {code}\n
        Request To: {request_url}\n
        \n
        Error: {message}
        """

        self.message = text.format(request_type=request_type, code=code, request_url=request_url, message=message)

    def __str__(self):
        return self.message
