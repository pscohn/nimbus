#!/usr/bin/env python3
import os
import datetime
import re
import markdown
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('templates'))

from models import *
import utils

def generate_posts(posts):
    if 'site' not in os.listdir():
        os.mkdir('site')

    if 'posts' in os.listdir('site'):
        utils.remove_existing()
    else:
        os.mkdir('site/posts')

    for post in posts:
        template = env.get_template('post.html')
        html = template.render({'post': post})
        f = open('site/posts/' + post.slug + '.html', 'w')
        print(html, file=f)
        f.close()

def generate_pages(pages, posts):
    if 'site' not in os.listdir():
        os.mkdir('site')

    for page in pages:
        template = env.get_template('page.html')
        html = template.render({'page': page, 'pages': pages, 'posts': posts})
        target = os.path.join('site', page.path)
        if os.path.exists(target):
            os.remove(target)
        f = open(target, 'w')
        print(html, file=f)
        f.close()

def read_posts():
    postnames = []
    posts = []
    for post in os.listdir('input'):
        if post[0] != '.' and post[-5:] == '.html':
            postnames.append(post)
            posts.append(open('input/' + post).read())
    post_objects = []
    for i, post in enumerate(posts):
        split = post.split('\n')
        title = split[0].strip()
        body = markdown.markdown('\n'.join(split[1:]).strip())
        namesplit = postnames[i].split('-')
        year, month, day = namesplit[:3]
        slug = '-'.join(namesplit[3:])[:-5] # strip .html from end
        date = datetime.date(int(year), int(month), int(day))
        post_objects.append(Post(title, slug, date, body))
    return post_objects

def read_pages():
    postnames = []
    posts = []
    for post in os.listdir('pages'):
        if post[0] != '.' and post[-5:] == '.html':
            postnames.append(post)
            posts.append(open('pages/' + post).read())
    post_objects = []
    for i, post in enumerate(posts):
        split = post.split('\n')
        title = split[0].strip()
        body = markdown.markdown('\n'.join(split[1:]).strip())
        path = postnames[i]
        post_objects.append(Page(title, body, path))
    return post_objects

def main():
    posts = read_posts()
    pages = read_pages()
    generate_posts(posts)
    generate_pages(pages, posts)
    utils.printnum(len(posts), 'post')
    utils.printnum(len(pages), 'page')

if __name__ == '__main__':
    main()
