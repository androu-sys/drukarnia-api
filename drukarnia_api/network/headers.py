from typing import Dict
from fake_useragent import UserAgent


class Headers(dict):
    def __init__(self,  **kwargs):
        """
        Initialize the Headers object.

        Parameters:
            dynamic_user_generation (bool):
               If True, enables dynamic generation of the User-Agent header using fake_useragent.
               If False, uses a static User-Agent header generated once during initialization.
               Defaults to False.
            **kwargs: Additional headers as key-value pairs.

        Returns:
            None
        """
        super().__init__(**{
            'Content-Type': 'application/json',
            'User-Agent': UserAgent().random,
        })

        self.update(kwargs)
