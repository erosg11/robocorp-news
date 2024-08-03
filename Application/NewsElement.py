from pydantic import BaseModel
from datetime import datetime


class NewsElement(BaseModel):
    title: str | None = None
    description: str | None = None
    date: datetime | None = None
    picture_url: str | None = None
