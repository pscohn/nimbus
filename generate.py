#!/usr/bin/env python3
import os
import math
from feedgen.feed import FeedGenerator
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('templates'))

from models import *
import reader
import config
import utils

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

def main():
    posts = reader.read_posts()[::-1]
    pages = reader.read_pages()
    index = reader.read_index()
    generate_posts(posts, pages)
    generate_pages(pages, posts)
    generate_index(pages, posts, index)
    generate_feed(posts)
    utils.printnum(len(posts), 'post')
    utils.printnum(len(pages), 'page')

if __name__ == '__main__':
    main()
