from typing import Dict
from fake_useragent import UserAgent


class Headers(dict):
    def __init__(self, dynamic_user_generation: bool = False, **kwargs):
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
        super(Headers, self).__init__(**{'Content-Type': 'application/json'})

        self.update(kwargs)

        if dynamic_user_generation:
            self.__setitem__('User-Agent', lambda: UserAgent().random)
        else:
            self.__setitem__('User-Agent', UserAgent().random)

    @property
    def static(self) -> Dict:
        """
        Return a dictionary containing the static headers.

        If a header value is callable, it will be executed to generate the actual value.

        Returns:
            Dict: A dictionary containing the static headers.
        """
        return {k: v() if callable(v) else v for k, v in self.items()}
