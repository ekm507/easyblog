import jinja2

from models import BlogInfo, PostListDetail


def generate_feed(
    blog_info: BlogInfo,
    posts_list: list[PostListDetail],
    template: jinja2.Template,
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
