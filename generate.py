#!/bin/env python3

import os
import re
import shutil
import tomllib
from pathlib import Path
from urllib.parse import urljoin

import jdatetime
import jinja2
from markdown_it import MarkdownIt

from feedgen import generate_feed
from models import BlogInfo, PostDetail, PostListDetail

OUTPUT_DIR = Path("output")
CONTENT_DIR = Path("content")
BLOG_DIR = OUTPUT_DIR / "blog"

TEMPLATES_PATHS = {
    "index_html": "index.html",
    "post_html": "post.html",
}

STYLES_DIR = Path("theme/css")
ASSETS_DIR = Path("theme/assets")

template_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader("theme/"),
)


def read_post_from_markdown(md_text: str) -> PostDetail:
    lines = md_text.split("---\n")
    header_lines = lines[0]
    body_text = "---\n".join(lines[1:])
    try:
        title = re.search(r"(?:title|عنوان) *: *(?P<title>.*)", header_lines).group(
            "title"
        )
    except AttributeError as err:
        # TODO: show file name in error message
        raise ValueError("post does not have title or title is invalid !") from err

    try:
        date_str = re.search(
            r"(?:date|تاریخ) *: *(?P<date>\d{4}-\d{1,2}-\d{1,2})", header_lines
        ).group("date")
    except AttributeError as err:
        # TODO: show file name in error message
        raise ValueError("post does not have date or date is invalid !") from err

    date_vars = [int(item) for item in date_str.split("-")]
    jdate = jdatetime.date(
        year=date_vars[0],
        month=date_vars[1],
        day=date_vars[2],
        locale=jdatetime.FA_LOCALE,
    )

    mdparser = MarkdownIt()
    body_html = mdparser.render(body_text)
    post_object = PostDetail(title=title, content=body_html, published_date=jdate)

    return post_object


def generate_index_html(
    post_details: list[PostListDetail],
) -> str:
    # generate index.html content
    post_details.sort(key=lambda p: p.published_date, reverse=True)
    # TODO: set constants for paths
    template = template_environment.get_template(name=TEMPLATES_PATHS["index_html"])
    output = template.render(posts=post_details)

    return output


def generate_post_html(
    post_detail: PostDetail,
) -> str:
    # generate post.html file content
    # TODO: set constants for paths
    template = template_environment.get_template(name=TEMPLATES_PATHS["post_html"])
    output = template.render(post=post_detail)

    return output


def read_file(file_path: Path | str) -> str:
    with open(file_path) as file:
        content = file.read()
    return content


def write_file(file_path: Path | str, content: str) -> None:
    with open(file_path, "w") as file:
        file.write(content)


def copy_dir(src_dir: str | Path, dest_dir: str | Path) -> None:
    # Ensure the destination parent directory exists
    dest_path = os.path.join(dest_dir, os.path.basename(src_dir))

    # Copy the entire directory recursively
    shutil.copytree(src_dir, dest_path, dirs_exist_ok=True)


if __name__ == "__main__":
    # read config file
    with open("config.toml", "rb") as file:
        config_data = tomllib.load(file)

    blog_info = BlogInfo(
        title=config_data["title"],
        description=config_data["description"],
        website_url=config_data["base_url"],
        feed_url=urljoin(config_data["base_url"], "rss.xml"),
    )
    should_generate_feed: bool = config_data["generate_feed"]
    # set blog title in base.html
    template_environment.globals["website_title"] = blog_info.title
    # define static files prefix
    static_prefix_url = blog_info.website_url
    static_prefix_url = (
        static_prefix_url
        if static_prefix_url.endswith("/")
        else static_prefix_url + "/"
    )
    template_environment.globals["STATIC_PREFIX"] = static_prefix_url

    # create output directories
    OUTPUT_DIR.mkdir(exist_ok=True, parents=True)
    BLOG_DIR.mkdir(exist_ok=True, parents=True)

    # copy static data directories
    copy_dir(STYLES_DIR, OUTPUT_DIR)
    copy_dir(ASSETS_DIR, OUTPUT_DIR)
    copy_dir(CONTENT_DIR / "img/", OUTPUT_DIR)
    # TODO: copy any other html files (non-template)

    # read contents
    posts_list_details: list[PostListDetail] = []

    for md_filename in CONTENT_DIR.glob("*.md"):
        # read markdown and convert to html
        mdfile_text = read_file(file_path=md_filename)
        post_detail = read_post_from_markdown(md_text=mdfile_text)
        post_html_content = generate_post_html(post_detail=post_detail)

        # write html output
        output_file_path = BLOG_DIR / md_filename.name.replace(
            md_filename.suffix, ".html"
        )
        write_file(file_path=output_file_path, content=post_html_content)
        posts_list_details.append(
            PostListDetail(
                title=post_detail.title,
                url="/".join(
                    output_file_path.parts[1:]
                ),  # get path after output directory
                published_date=post_detail.published_date,
            )
        )
        print("new content file added :", output_file_path)

    # generate index.html
    index_html_content = generate_index_html(post_details=posts_list_details)
    index_html_path = OUTPUT_DIR / "index.html"
    write_file(file_path=index_html_path, content=index_html_content)
    print("indexfile created at :", index_html_path)

    # generate rss feed
    if should_generate_feed:
        feed_content = generate_feed(blog_info=blog_info, posts_list=posts_list_details)
        feed_output_path = OUTPUT_DIR / "rss.xml"
        with open(feed_output_path, "w") as file:
            file.write(feed_content)

        print("rss feed generated :", feed_output_path)
