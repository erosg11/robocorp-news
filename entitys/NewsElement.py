from pathlib import Path
from typing import Literal

from pydantic import BaseModel
from datetime import datetime


class NewsElement(BaseModel):
    """
    An class that represents a news element.
    :param title: The title of the news element.
    :param description: The description of the news element.
    :param date: The date the news element was published.
    :param picture_url: The url of the news element picture.
    :param search_phrase: The search phrase used to find the news element.
    :param file: The file path of the news element picture.
    :param filename: The filename of the news element picture.
    :param count_matches: The number of time that search_phrase was found in the news element.
    :param has_dollars: If was found dollars amount specified in the news element.
    """
    title: str | None = None
    description: str | None = None
    date: datetime | None = None
    picture_url: str | None = None
    search_phrase: str | None = None
    file: Path | None = None
    filename: str | None = None
    count_matches: int | None = None
    has_dollars: Literal['TRUE', 'FALSE'] | None = None
