from pydantic import BaseModel


class ImageLink(BaseModel):
    url: str
    img_src: str


class Unit(BaseModel):
    title: str
    description: str
    lectures: list[ImageLink]
    video_content: list[ImageLink]
    additional_resources: list[str]


class EconData(BaseModel):
    welcome: str
    units: list[Unit]
