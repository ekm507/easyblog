import jinja2
from models import BlogInfo, PostListDetail


environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader("theme/"),
)
template = environment.get_template("rss.xml.jinja")


def generate_feed(
    blog_info: BlogInfo,
    posts_list: list[PostListDetail],
) -> str:
    # render template
    content = template.render(
        title=blog_info.title,
        description=blog_info.description,
        website_url=blog_info.website_url,
        feed_url=blog_info.feed_url,
        posts=posts_list,
    )

    return content
