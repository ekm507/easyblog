from dataclasses import dataclass
from datetime import date

import jdatetime


def english_to_farsi_nums(text: str) -> str:
    nums_map = {
        "0": "۰",
        "1": "۱",
        "2": "۲",
        "3": "۳",
        "4": "۴",
        "5": "۵",
        "6": "۶",
        "7": "۷",
        "8": "۸",
        "9": "۹",
    }

    for en in nums_map:
        text = text.replace(en, nums_map[en])

    return text


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

    @property
    def published_date_geo(self) -> date:
        return self.published_date.togregorian()

    @property
    def published_date_str(
        self,
    ) -> str:
        jdate_str = english_to_farsi_nums(self.published_date.strftime("%d %b %Y"))

        return jdate_str


@dataclass
class PostDetail:
    title: str
    content: str
    published_date: jdatetime.date
