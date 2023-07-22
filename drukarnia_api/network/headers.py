from typing import Dict
from fake_useragent import UserAgent


class Headers(dict):
    def __init__(self, dynamic_user_generation: bool = False, **kwargs):
        super(Headers, self).__init__(**{'Content-Type': 'application/json'})

        self.update(kwargs)

        if dynamic_user_generation:
            self.__setitem__('User-Agent', lambda: UserAgent().random)

        else:
            self.__setitem__('User-Agent', UserAgent().random)

    @property
    def static(self) -> Dict:
        return {k: v() if callable(v) else v for k, v in self.items()}


