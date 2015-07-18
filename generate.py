#!/usr/bin/env python3
import os
import datetime
import re
import math
import markdown
from feedgen.feed import FeedGenerator
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('templates'))

from models import *
import config
import utils

def generate_posts(posts, pages):
    if 'site' not in os.listdir():
        os.mkdir('site')

    if 'posts' in os.listdir('site'):
        utils.remove_existing()
    else:
        os.mkdir('site/posts')

    for post in posts:
        template = env.get_template('post.html')
        html = template.render({'menu': config.menu, 'post': post, 'pages': pages, 'site_title': config.site_title})
        while os.path.exists(os.path.join('site/posts', post.slug + '.html')):
            post.slug = post.slug + '-%s%s%s' % (post.date.year, post.date.month, post.date.day)
        f = open('site/posts/' + post.slug + '.html', 'w')
        print(html, file=f)
        f.close()

def generate_feed(posts):
    author = {'name': config.author, 'email': config.email}
    fg = FeedGenerator()
    fg.id('http://%s/rss.xml' % config.domain)
    fg.title('%s RSS Feed' % config.domain)
    fg.author(author)
    fg.link(href='http://%s' % config.domain, rel='alternate')
    fg.language('en')
    fg.description('%s RSS Feed' % config.domain)

    for post in posts[:10]:
        fe = fg.add_entry()
        fe.id('http://%s/posts/%s.html' % (config.domain, post.slug))
        fe.title(post.title)
        fe.content(content=post.body, type='html')
        fe.author(author)

    rssfeed = fg.rss_str(pretty=True)
    fg.rss_file('site/rss.xml')

def generate_pages(pages, posts):
    if 'site' not in os.listdir():
        os.mkdir('site')

    for page in pages:
        template = env.get_template('page.html')
        html = template.render({'menu': config.menu, 'page': page, 'pages': pages, 'posts': posts, 'site_title': config.site_title})
        target = os.path.join('site', page.path)
        if os.path.exists(target):
            os.remove(target)
        f = open(target, 'w')
        print(html, file=f)
        f.close()

def generate_index(pages, posts, index):
    template = env.get_template('index.html')
    max_pages = math.ceil(len(posts) / config.paginate_by)
    for i in range(0, max_pages):
        
        html = template.render({'page': index, 
                                'pages': pages,
                                'posts': posts[i*config.paginate_by:(i+1)*config.paginate_by],
                                'menu': config.menu,
                                'site_title': config.site_title,
                                'index': i+1, 
                                'max_pages': max_pages
                              })
        if i == 0:
            target = os.path.join('site', index.path)
        else:
            target = os.path.join('site', 'index_%s.html' % str(i + 1))
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
        if post[0] != '.' and post[-5:] == '.html' and post != 'index.html':
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

def read_index():
    name = 'index.html'
    post = open('pages/' + name).read()
    split = post.split('\n')
    title = split[0].strip()
    body = markdown.markdown('\n'.join(split[1:]).strip())
    path = 'index.html'
    return Page(title, body, path)

def main():
    posts = read_posts()[::-1]
    pages = read_pages()
    index = read_index()
    generate_posts(posts, pages)
    generate_pages(pages, posts)
    generate_index(pages, posts, index)
    generate_feed(posts)
    utils.printnum(len(posts), 'post')
    utils.printnum(len(pages), 'page')

if __name__ == '__main__':
    main()
