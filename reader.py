import os
import datetime

import markdown

from models import *
import config

def read(folder):
    filenames = []
    contents = []
    for filename in os.listdir(folder):
        if filename[0] != '.' and filename[-5:] == '.html' and filename != 'index.html':
            filenames.append(filename)
            contents.append(open('%s/' % folder + filename).read())
    return filenames, contents

def parse_filename(filename):
    split = filename.split('-')
    slug = '-'.join(split[3:])[:-5] # strip .html from end
    year, month, day = split[:3]
    date = datetime.date(int(year), int(month), int(day))
    return slug, date

def parse_content(content):
    split = content.split('\n')
    title = split[0].strip()
    body = markdown.markdown('\n'.join(split[1:]).strip())
    return title, body

def read_posts():
    postnames, posts = read(config.posts_path)

    post_objects = []
    for i, post in enumerate(posts):
        slug, date = parse_filename(postnames[i])
        title, body = parse_content(post)
        post_objects.append(Post(title, slug, date, body))
    return post_objects

def read_pages():
    postnames, posts = read(config.pages_path)

    post_objects = []
    for i, post in enumerate(posts):
        path = postnames[i]
        title, body = parse_content(post)
        post_objects.append(Page(title, body, path))
    return post_objects

def read_index():
    name = 'index.html'
    post = open('%s/' % config.pages_path + name).read()
    split = post.split('\n')
    title = split[0].strip()
    body = markdown.markdown('\n'.join(split[1:]).strip())
    path = 'index.html'
    return Page(title, body, path)
