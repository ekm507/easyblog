from markdown_it import MarkdownIt
import re
import os
import shutil


def md_to_html(mdfile_text, html_template):
    lines = mdfile_text.split('---\n')
    header_lines = lines[0]
    body_text = '---\n'.join(lines[1:])
    try:
        title = re.findall('title *: *(.*)', header_lines)[0]
    except IndexError:
        title = "***"
        print(f"post does not have title. set to ***")
    try:
        date = re.findall('date *: *(.*)', header_lines)[0]
    except IndexError:
        date = '1400-01-01'
        print("post does not have date. set to ***")

    
    mdparser = MarkdownIt()
    body_html = mdparser.render(body_text)

    output = html_template.replace("TITLE", title).replace("POST", body_html)
    
    return output, title, date


def generate_index(index_html_template, index_post_list_template, post_details):
    posts_html_list = ''
    for post in post_details:
        title, link, date = post
        post_part = index_post_list_template.replace("TITLE", title).replace("LINK", link).replace("DATE", date)
        posts_html_list += post_part
    
    output = index_html_template.replace("POSTS", posts_html_list)
    return output

html_post_template_filename = 'theme/post.html'
html_index_template_filename = 'theme/index.html'
html_index_post_list_template_filename = 'theme/index_post_list.html'

html_post_template = open(html_post_template_filename).read()
html_index_template = open(html_index_template_filename).read()
html_index_post_list_template = open(html_index_post_list_template_filename).read()

shutil.copy('theme/post_stylesheet.css', 'output')
shutil.copy('theme/index_stylesheet.css', 'output')

mdfiles = list(filter(lambda x:x.endswith('.md'), os.listdir('content')))

posts_details = []
for md_filename in mdfiles:
    mdfile_text = open(f"content/{md_filename}").read()
    post_html, title, date = md_to_html(mdfile_text, html_post_template)
    outfilename = f"output/{md_filename[:-3]}.html"
    open(outfilename, 'w').write(post_html)
    posts_details.append((title, md_filename[:-3]+'.html', date))

index_html = generate_index(html_index_template, html_index_post_list_template, posts_details)
outfilename = f"output/index.html"
open(outfilename, 'w').write(index_html)

