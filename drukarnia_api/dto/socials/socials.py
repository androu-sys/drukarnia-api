from attr import define, field, validators


@define
class Socials:
    name: str = field(
        validator=validators.instance_of(str),
    )
    url: str = field(
        validator=validators.instance_of(str),
    )
