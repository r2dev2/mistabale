from typing import NamedTuple


class ImageLink(NamedTuple):
    url: str
    img_src: str


class Unit(NamedTuple):
    title: str
    description: str
    lectures: list[ImageLink]
    video_content: list[ImageLink]
    additional_resources: list[str]

class EconData(NamedTuple):
    welcome: str
    units: list[Unit]
