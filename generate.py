#!/usr/bin/env python3
import os
import datetime
import re

var_regex = re.compile(r'{{ ?\S+ ?}}')

class Post:
    def __init__(self, title, slug, date, body):
        self.title = title
        self.slug = slug
        self.body = body
        self.date = date

def fread(path):
    f = open(path)
    content = f.read()
    f.close()
    return content

def remove_existing():
    for post in os.listdir('site/posts'):
        os.remove('site/posts/' + post)

def render(template_name, context):
    html = open('templates/' + template_name).read()
    for f in re.finditer(var_regex, html):
        varname = f.group().strip(' {}')
        if '.' in varname:
            elem = varname.split('.')
            html = html.replace(f.group(), getattr(context[elem[0]], elem[1]))
        else:
            html = html.replace(f.group(), getattr(context[elem]))
    return html

def generate_html(posts):
    if 'site' not in os.listdir():
        os.mkdir('site')

    if 'posts' in os.listdir('site'):
        remove_existing()
    else:
        os.mkdir('site/posts')

    for post in posts:
        html = render('post.html', {'post': post})
        f = open('site/posts/' + post.slug + '.html', 'w')
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
        body = '\n'.join(split[1:]).strip()
        namesplit = postnames[i].split('-')
        year = namesplit[0]
        month = namesplit[1]
        day = namesplit[2]
        slug = '-'.join(namesplit[3:])[:-5] # strip .html from end
        date = datetime.date(int(year), int(month), int(day))
        post_objects.append(Post(title, slug, date, body))
    return post_objects

def main():
    posts = read_posts()
    generate_html(posts)
    num = len(posts)
    if num == 1:
        print('generated 1 post')
    else:
        print('generated %s posts' % num)

if __name__ == '__main__':
    main()
