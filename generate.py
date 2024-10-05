from datetime import date
from typing import TypeAlias
from markdown_it import MarkdownIt
from pathlib import Path
import re
import os
import shutil
import jdatetime
from feedgen import generate_feed, BlogInfo, PostDetail as PostListDetail


PostDetail: TypeAlias = tuple[str, str, jdatetime.datetime]


BLOG_INFO: BlogInfo = {
    "title": "My Blog Name",
    "description": "Add here some description",
    "website_url": "https://example.com/blog",
    "feed_url": "https://example.com/blog/rss.xml",
}


def english_to_farsi_nums(num: str):
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
    return "".join(list(map(lambda x: nums_map[x], num)))


def md_to_html(mdfile_text: str, html_template: str) -> PostDetail:
    lines = mdfile_text.split("---\n")
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

    jdate = jdatetime.datetime.fromisoformat(date)

    mdparser = MarkdownIt()
    body_html = mdparser.render(body_text)

    output = html_template.replace("TITLE", title).replace("POST", body_html)

    return output, title, jdate


def get_jdate_str(jdate: jdatetime.datetime) -> str:
    jday = english_to_farsi_nums(str(jdate.day))
    jmonth = jdate.j_months_fa[jdate.month - 1]
    jyear = english_to_farsi_nums(str(jdate.year))
    jdate_str = f"{jday} {jmonth} {jyear}"

    return jdate_str


def generate_index(
    index_html_template: str,
    index_post_list_template: str,
    post_details: list[PostDetail],
) -> str:
    post_details.sort(key=lambda a: a[2], reverse=True)

    posts_html_list = ""
    for post in post_details:
        title, link, date = post
        post_part = (
            index_post_list_template.replace("TITLE", title)
            .replace("LINK", link)
            .replace("DATE", get_jdate_str(date))
        )
        posts_html_list += post_part

    output = index_html_template.replace("POSTS", posts_html_list)
    return output


def copy_all(srcdir: str | Path, dstdir: str | Path) -> None:
    os.makedirs(dstdir, exist_ok=True)
    for q in os.listdir(srcdir):
        shutil.copy(os.path.join(srcdir, q), dstdir)


if __name__ == "__main__":
    html_post_template_filename = "theme/post.html"
    html_index_template_filename = "theme/index.html"
    html_index_post_list_template_filename = "theme/index_post_list.html"

    with (
        open(html_post_template_filename) as html_post_template_file,
        open(html_index_template_filename) as html_index_template_file,
        open(
            html_index_post_list_template_filename
        ) as html_index_post_list_template_file,
    ):
        # read files
        html_post_template = html_post_template_file.read()
        html_index_template = html_index_template_file.read()
        html_index_post_list_template = html_index_post_list_template_file.read()

    os.makedirs("output", exist_ok=True)
    # copy_all('theme/', )
    shutil.copy("theme/post_stylesheet.css", "output")
    shutil.copy("theme/index_stylesheet.css", "output")

    copy_all("content/img/", "output/img/")

    mdfiles = list(filter(lambda x: x.endswith(".md"), os.listdir("content")))

    posts_details: list[PostDetail] = []
    for md_filename in mdfiles:
        with (
            open(f"content/{md_filename}") as md_file,
            open(f"output/{md_filename[:-3]}.html", "w") as output_file,
        ):
            # read markdown and convert to html
            mdfile_text = md_file.read()
            post_html, title, jalali_date = md_to_html(mdfile_text, html_post_template)
            # write html output
            output_file.write(post_html)
            posts_details.append(
                (
                    title,
                    md_filename[:-3] + ".html",
                    jalali_date,
                )
            )
            print("new content file added :", md_filename)

    # generate index.html
    index_html = generate_index(
        html_index_template, html_index_post_list_template, posts_details
    )
    with open("output/index.html", "w") as index_html_file:
        index_html_file.write(index_html)

    print("index.html file created !")

    # generate rss feed
    posts_list: list[PostListDetail] = [
        {
            "title": p[0],
            "url": p[1],
            "pub_date": date(year=p[2].year, month=p[2].month, day=p[2].day),
        }
        for p in posts_details
    ]
    feed_content = generate_feed(blog_info=BLOG_INFO, posts_list=posts_list)
    feed_output_path = Path("output/rss.xml")
    with open(feed_output_path, "w") as file:
        file.write(feed_content)

    print("rss feed generated :", feed_output_path)
