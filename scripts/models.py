from typing import List

from pydantic import BaseModel


class ImageLink(BaseModel):
    url: str
    img_src: str


class TextLink(BaseModel):
    url: str
    text: str


class Unit(BaseModel):
    title: str
    description: str
    resources: List[ImageLink]
    documents: List[List[TextLink]]


class EconData(BaseModel):
    welcome: str
    units: List[Unit]
