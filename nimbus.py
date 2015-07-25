#!/usr/bin/env python3
import os
import sys
import math
from feedgen.feed import FeedGenerator
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))

from models import *
import reader
import utils

import configparser
config = configparser.ConfigParser()
config.read(os.path.join(os.getcwd(), 'nimbus.ini'))

def generate_feed(posts):
    author = {'name': config['default']['author'], 'email': config['default']['email']}
    fg = FeedGenerator()
    fg.id('http://%s/rss.xml' % config['default']['domain'])
    fg.title('%s RSS Feed' % config['default']['domain'])
    fg.author(author)
    fg.link(href='http://%s' % config['default']['domain'], rel='alternate')
    fg.language('en')
    fg.description('%s RSS Feed' % config['default']['domain'])

    for post in posts[:10]:
        fe = fg.add_entry()
        fe.id('http://%s/posts/%s.html' % (config['default']['domain'], post.slug))
        fe.title(post.title)
        fe.content(content=post.body, type='html')
        fe.author(author)

    rssfeed = fg.rss_str(pretty=True)
    fg.rss_file(os.path.join(config['default']['site_path'], 'rss.xml'))

def generate_posts(posts, pages):
    if not os.path.exists(config['default']['site_path']):
        os.mkdir(config['default']['site_path'])

    if 'posts' in os.listdir(config['default']['site_path']):
        utils.remove_existing(os.path.join(config['default']['site_path'], 'posts'))
    else:
        os.mkdir(os.path.join(config['default']['site_path'], 'posts'))

    for post in posts:
        template = env.get_template('post.html')
        html = template.render({'menu': config['menu'], 'post': post, 'pages': pages, 'site_title': config['default']['site_title']})
        while os.path.exists(os.path.join(config['default']['site_path'], 'posts', post.slug + '.html')):
            post.slug = post.slug + '-%s%s%s' % (post.date.year, post.date.month, post.date.day)
        f = open(os.path.join(config['default']['site_path'], 'posts', post.slug + '.html'), 'w')
        print(html, file=f)
        f.close()

def generate_pages(pages, posts):
    if not os.path.exists(config['default']['site_path']):
        os.mkdir(config['default']['site_path'])

    for page in pages:
        template = env.get_template('page.html')
        html = template.render({'menu': config['menu'], 'page': page, 'pages': pages, 'posts': posts, 'site_title': config['default']['site_title']})
        target = os.path.join(config['default']['site_path'], page.path)
        if os.path.exists(target):
            os.remove(target)
        f = open(target, 'w')
        print(html, file=f)
        f.close()

def generate_index(pages, posts, index):
    template = env.get_template('index.html')
    paginate = int(config['default']['paginate_by'])
    max_pages = math.ceil(len(posts) / paginate)
    for i in range(0, max_pages):
        
        html = template.render({'page': index, 
                                'pages': pages,
                                'posts': posts[i*paginate:(i+1)*paginate],
                                'menu': config['menu'],
                                'site_title': config['default']['site_title'],
                                'index': i+1, 
                                'max_pages': max_pages
                              })
        if i == 0:
            target = os.path.join(config['default']['site_path'], index.path)
        else:
            target = os.path.join(config['default']['site_path'], 'index_%s.html' % str(i + 1))
        if os.path.exists(target):
            os.remove(target)
        f = open(target, 'w')
        print(html, file=f)
        f.close()

def generate():
    posts = reader.read_posts(config['default']['posts_path'])[::-1]
    pages = reader.read_pages(config['default']['pages_path'])
    index = reader.read_index(config['default']['pages_path'])
    generate_posts(posts, pages)
    generate_pages(pages, posts)
    generate_index(pages, posts, index)
    generate_feed(posts)
    utils.printnum(len(posts), 'post')
    utils.printnum(len(pages), 'page')

def init():
    folder = os.environ['PWD']
    if os.path.exists(os.path.join(folder, '.static.py')):
        print('project already exists')
        return

    config = '''\
site_title = 'Site Title'
author = 'Your Name'
domain = 'yourdomain.com'
email = 'your@email.com'
paginate_by = 5
pages_path = 'pages'
posts_path = 'input'
site_path = 'site'
menu = (('About', '/about.html'),
        ('GitHub', 'http://github.com/pscohn'),
        ('Email', 'mailto:pscohn@gmail.com'),
    )
    '''

    f = open('.static.py', 'w')
    print(config, file=f)
    f.close()

import http.server
import socketserver
def main():
    if len(sys.argv) == 1:
        return

    if sys.argv[1] == 'init':
        init()

    if sys.argv[1] == 'generate':
        generate()

    if sys.argv[1] == 'run':
        os.chdir(config['default']['site_path'])
        handler = http.server.SimpleHTTPRequestHandler
        httpd = socketserver.TCPServer(("", 8080), handler)
        httpd.serve_forever()

if __name__ == '__main__':
    main()
