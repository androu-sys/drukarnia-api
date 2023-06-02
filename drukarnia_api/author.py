from drukarnia_api.connection import GetRequest
import asyncio

from aiohttp import ClientSession
from typing import List


class Author:
    session = None
    data = None

    def collect_followers(self, batch_size: int = 5) -> List['Author']:
        if '_id' not in self.data:
            raise ValueError('Author data does not contain _id.')

        elif not self.session:
            raise ValueError('Author session is not initialized.')

        api_request = '/api/relationships/{user_id}/followers?'.format(user_id=self.data['_id'])

        all_followers = []
        iter_ = 0

        while True:
            api_requests = [api_request + f'page={page}'
                            for page in range(iter_ * batch_size + 1,
                                              (iter_ + 1) * batch_size + 1)]

            loop = asyncio.get_event_loop()
            follower_pages = loop.run_until_complete(
                GetRequest.get_pool(self.session, api_requests)
            )

            follower_pages = [page for page in follower_pages if page]

            new_followers = [Author.from_data(session=self.session, data=follower)
                             for page in follower_pages
                             for follower in page]

            all_followers.extend(new_followers)
            iter_ += 1

            if len(follower_pages) != batch_size:
                break

        return all_followers

    def collect_followings(self, batch_size: int = 5) -> List['Author']:
        if '_id' not in self.data:
            raise ValueError('Author data does not contain _id.')

        elif not self.session:
            raise ValueError('Author session is not initialized.')

        api_request = '/api/relationships/{user_id}/following?'.format(user_id=self.data['_id'])

        all_followings = []
        iter_ = 0

        while True:
            api_requests = [api_request + f'page={page}'
                            for page in range(iter_ * batch_size + 1,
                                              (iter_ + 1) * batch_size + 1)]

            loop = asyncio.get_event_loop()
            followings_pages = loop.run_until_complete(
                GetRequest.get_pool(self.session, api_requests)
            )

            followings_pages = [page for page in followings_pages if page]

            new_followings = [Author.from_data(session=self.session, data=following)
                              for page in followings_pages
                              for following in page]

            all_followings.extend(new_followings)
            iter_ += 1

            if len(followings_pages) != batch_size:
                break

        return all_followings

    @staticmethod
    def find_author(session: ClientSession, username) -> 'Author':
        url = '/api/users/profile/{username}'.format(username=username)

        loop = asyncio.get_event_loop()
        data = loop.run_until_complete(GetRequest.get(session, url))

        author = Author()
        author.session, author.data = session, data

        return author

    @staticmethod
    def from_data(session: ClientSession, data: dict) -> 'Author':
        author = Author()
        author.session, author.data = session, data

        return author
