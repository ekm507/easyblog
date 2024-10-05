from datetime import date
from typing import TypedDict
import jinja2


class BlogInfo(TypedDict):
    title: str
    description: str
    website_url: str
    feed_url: str


class PostDetail(TypedDict):
    title: str
    url: str
    pub_date: date


environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader("theme/"),
)
template = environment.get_template("rss.xml.jinja")


def generate_feed(
    blog_info: BlogInfo,
    posts_list: list[PostDetail],
) -> str:
    # render template
    content = template.render(
        title=blog_info["title"],
        description=["url"],
        website_url=blog_info["website_url"],
        feed_url=blog_info["feed_url"],
        posts=posts_list,
    )

    return content
