from aiohttp import ClientSession
from drukarnia_api.drukarnia_base.element import DrukarniaElement


class Tag(DrukarniaElement):
    def __init__(self, slug_name: str = None, tag_id: str = None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Update the data with slug_name and tag_id
        self._update_data({'slug': slug_name, '_id': tag_id})

    @property
    def slug(self):
        """
        Get the slug property of the Tag.
        """
        return self._access_data('slug', str)

    @property
    def created_at(self):
        """
        Get the created_at property of the Tag.
        """
        return self._get_datetime_from_author_data('createdAt')

    @property
    def default(self):
        """
        Get the default property of the Tag.
        """
        return self._get_basetype_from_data('default', bool)

    @property
    def mentions_num(self):
        """
        Get the mentions_num property of the Tag.
        """
        return self._get_basetype_from_data('mentionsNum', int)

    @property
    def name(self):
        """
        Get the name property of the Tag.
        """
        return self._access_data('name', None)

    @property
    def _id(self):
        """
        Get the _id property of the Tag.
        """
        return self._access_data('_id', None)

    @staticmethod
    async def from_records(session: ClientSession, new_data: dict) -> 'Tag':
        """
        Create a new Tag instance from records.

        Args:
            session (ClientSession): A session object for making HTTP requests.
            new_data (dict): Data to update the new Tag instance with.

        Returns:
            Tag: A new instance of the Tag class.
        """
        new_tag = Tag(session=session)
        new_tag._update_data(new_data)

        return new_tag
