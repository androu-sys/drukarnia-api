from typing import Optional
from drukarnia_api.dto.base import BaseDTO
from drukarnia_api.dto.utils import starts_with
from attrs import frozen, field, validators


@frozen
class SocialsDTO(BaseDTO):
    telegram: Optional[str] = field(
        validator=validators.optional(
            starts_with("https://t.me/")
        )
    )
    instagram: Optional[str] = field(
        validator=validators.optional((
            validators.instance_of(str),
            starts_with("https://instagram.com/")
        ))
    )

    twitter: Optional[str] = field(
        validator=validators.optional((
            validators.instance_of(str),
            starts_with("https://x.com/")
        ))
    )

    bluesky: Optional[str] = field(
        validator=validators.optional((
            validators.instance_of(str),
            starts_with("https://bsky.app/profile/")
        ))
    )

    facebook: Optional[str] = field(
        validator=validators.optional((
            validators.instance_of(str),
            starts_with("https://facebook.com/")
        ))
    )

    linkedin: Optional[str] = field(
        validator=validators.optional((
            validators.instance_of(str),
            starts_with("https://linkedin.com/")
        ))
    )

    youtube: Optional[str] = field(
        validator=validators.optional((
            validators.instance_of(str),
            starts_with("https://youtube.com/")
        ))
    )

    tiktok: Optional[str] = field(
        validator=validators.optional((
            validators.instance_of(str),
            starts_with("https://tiktok.com/")
        ))
    )

    website: Optional[str] = field(
        validator=validators.optional((
            validators.instance_of(str),
            starts_with("https://")
        ))
    )
