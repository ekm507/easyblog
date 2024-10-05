from dataclasses import dataclass
from datetime import date

import jdatetime


@dataclass
class BlogInfo:
    title: str
    description: str
    website_url: str
    feed_url: str


@dataclass
class PostListDetail:
    title: str
    url: str
    published_date: jdatetime.date
    published_date_geo: date
    published_date_str: str


@dataclass
class PostDetail:
    title: str
    content: str
    published_date: jdatetime.date
