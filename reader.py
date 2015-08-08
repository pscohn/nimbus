import os
import sys
import datetime

import markdown

from models import *

def _read(folder):
    filenames = []
    contents = []
    for filename in os.listdir(folder):
        if len(filename) < 4:
            continue

        if filename[0] != '.' and filename[-3:] == '.md' and filename != 'index.md':
            filenames.append(filename)
            contents.append(open('%s/' % folder + filename).read())

    return filenames, contents

def parse_filename(filename):
    split = filename.split('-')
    slug = '-'.join(split[3:])[:-3] # strip .html from end
    year, month, day = split[:3]
    date = datetime.date(int(year), int(month), int(day))
    return slug, date

def parse_content(content):
    split = content.split('\n')
    title = split[0].strip()
    body = markdown.markdown('\n'.join(split[1:]).strip())
    return title, body

def read_posts(path):
    postnames, posts = _read(path)

    post_objects = []
    for i, post in enumerate(posts):
        slug, date = parse_filename(postnames[i])
        title, body = parse_content(post)
        post_objects.append(Post(title, slug, date, body))
    return post_objects

def read_pages(path):
    pagenames, pages = _read(path)

    page_objects = []
    for i, post in enumerate(pages):
        path = pagenames[i][:-3] + '.html'
        title, body = parse_content(page)
        page_objects.append(Page(title, body, path))
    return page_objects
