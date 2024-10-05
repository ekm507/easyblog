import os
import re
import shutil
from pathlib import Path

import jdatetime
import jinja2
from markdown_it import MarkdownIt

from feedgen import generate_feed
from models import BlogInfo, PostDetail, PostListDetail

OUTPUT_DIR = Path("output")

BLOG_INFO = BlogInfo(
    title="My Blog Name",
    description="Add here some description",
    website_url="https://example.com/blog",
    feed_url="https://example.com/blog/rss.xml",
)

TEMPLATES_PATHS = {
    "index_html": "index.html",
    "post_html": "post.html",
}

environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader("theme/"),
)


def english_to_farsi_nums(num: str) -> str:
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
    return "".join([nums_map[x] for x in num])


def read_post_from_markdown(md_text: str) -> PostDetail:
    lines = md_text.split("---\n")
    header_lines = lines[0]
    body_text = "---\n".join(lines[1:])
    try:
        title = re.findall("(?:title|عنوان) *: *(.*)", header_lines)[0]
    except IndexError:
        title = "***"
        print("post does not have title. set to ***")
    try:
        date = re.findall("(?:date|تاریخ) *: *(.*)", header_lines)[0]
    except IndexError:
        date = "۱۴۰۰-۰۱-۰۱"
        print("post does not have date. set to ***")

    jdate = jdatetime.date.fromisoformat(date)

    mdparser = MarkdownIt()
    body_html = mdparser.render(body_text)
    post_object = PostDetail(title=title, content=body_html, published_date=jdate)

    return post_object


def get_jdate_str(jdate: jdatetime.date) -> str:
    jday = english_to_farsi_nums(str(jdate.day))
    jmonth = jdate.j_months_fa[jdate.month - 1]
    jyear = english_to_farsi_nums(str(jdate.year))
    jdate_str = f"{jday} {jmonth} {jyear}"

    return jdate_str


def generate_index_html(
    post_details: list[PostListDetail],
) -> str:
    # generate index.html content
    post_details.sort(key=lambda p: p.published_date, reverse=True)
    # TODO: set constants for paths
    template = environment.get_template(name=TEMPLATES_PATHS["index_html"])
    output = template.render(posts=post_details)

    return output


def generate_post_html(
    post_detail: PostDetail,
) -> str:
    # generate post.html file content
    # TODO: set constants for paths
    template = environment.get_template(name=TEMPLATES_PATHS["post_html"])
    output = template.render(post=post_detail)

    return output


def copy_all(srcdir: str | Path, dstdir: str | Path) -> None:
    os.makedirs(dstdir, exist_ok=True)
    for q in os.listdir(srcdir):
        shutil.copy(os.path.join(srcdir, q), dstdir)


def read_file(file_path: Path | str) -> str:
    with open(file_path) as file:
        content = file.read()
    return content


def write_file(file_path: Path | str, content: str) -> None:
    with open(file_path, "w") as file:
        file.write(content)


if __name__ == "__main__":
    # create output directory
    os.makedirs("output", exist_ok=True)
    # TODO: use static content for stylesheets in jinja templates
    # copy stylesheets
    shutil.copy("theme/post_stylesheet.css", "output")
    shutil.copy("theme/index_stylesheet.css", "output")

    # copy images
    copy_all("content/img/", "output/img/")

    # read contents
    posts_list_details: list[PostListDetail] = []

    for md_filename in Path("content").glob("*.md"):
        # read markdown and convert to html
        mdfile_text = read_file(file_path=md_filename)
        post_detail = read_post_from_markdown(md_text=mdfile_text)
        post_html_content = generate_post_html(post_detail=post_detail)

        # write html output
        output_file_path = OUTPUT_DIR / md_filename.name.replace(
            md_filename.suffix, ".html"
        )
        # TODO: create a seperate sub-directory for posts content
        write_file(file_path=output_file_path, content=post_html_content)
        posts_list_details.append(
            PostListDetail(
                title=post_detail.title,
                url=output_file_path.name,
                published_date=post_detail.published_date,
                published_date_str=get_jdate_str(jdate=post_detail.published_date),
                published_date_geo=post_detail.published_date.togregorian(),
            )
        )
        print("new content file added :", output_file_path)

    # generate index.html
    index_html_content = generate_index_html(post_details=posts_list_details)
    index_html_path = OUTPUT_DIR / "index.html"
    write_file(file_path=index_html_path, content=index_html_content)
    print("index.html file created !")

    # generate rss feed
    feed_content = generate_feed(blog_info=BLOG_INFO, posts_list=posts_list_details)
    feed_output_path = OUTPUT_DIR / "rss.xml"
    with open(feed_output_path, "w") as file:
        file.write(feed_content)

    print("rss feed generated :", feed_output_path)
