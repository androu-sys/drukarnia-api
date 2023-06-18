from aiohttp import ClientSession
from drukarnia_api.drukarnia_base.element import DrukarniaElement


class Tag(DrukarniaElement):
    def __init__(self, slug_name: str = None, tag_id: str = None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._update_data({'slug': slug_name, '_id': tag_id})

    @property
    def slug(self):
        return self._access_data('slug', str)

    @property
    def created_at(self):
        return self._get_datetime_from_author_data('createdAt')

    @property
    def default(self):
        return self._get_basetype_from_data('default', bool)

    @property
    def mentions_num(self):
        return self._get_basetype_from_data('mentionsNum', int)

    @property
    def name(self):
        return self._access_data('name', None)

    @property
    def _id(self):
        return self._access_data('_id', None)

    @staticmethod
    async def from_records(session: ClientSession, new_data: dict) -> 'Tag':
        """
        Create an Author instance from records.
        """

        new_tag = Tag(session=session)
        new_tag._update_data(new_data)

        return new_tag
