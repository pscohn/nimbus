import unittest
import datetime
import random
import shutil
import os

import models
import reader

exampleposts = [
    ('2015-07-01-test-post.md', 'Post Title\n\nPostBody'),
    ('2015-07-02-second-post.md', 'Post Title 2\n\nPostBody 2'),
]

examplepages = [
    ('about.md', 'About me\n\nHere is some info about me.'),
]

def setup_files():
    dirname = 'nimbustest-' + str(random.randrange(1000, 10000000))
    os.mkdir(dirname)
    os.mkdir(os.path.join(dirname, 'posts'))
    os.mkdir(os.path.join(dirname, 'pages'))
    for post in exampleposts:
        f = open(os.path.join(dirname, 'posts', post[0]), 'w')
        f.write(post[1])
        f.close()
    for page in examplepages:
        f = open(os.path.join(dirname, 'pages', page[0]), 'w')
        f.write(page[1])
        f.close()
    return dirname

def teardown(dirname):
    shutil.rmtree(dirname)

class ReaderTests(unittest.TestCase):
    def setUp(self):
        self.dirname = setup_files()

    def test_read(self):
        folder = os.path.join(self.dirname, 'posts')
        filenames, filebodys = reader._read(folder)
        self.assertEqual(len(exampleposts), len(filenames))
        self.assertEqual(filenames[0], exampleposts[0][0])
        self.assertEqual(filebodys[0], exampleposts[0][1])

    def test_read_files(self):
        posts = reader.read_files(os.path.join(self.dirname, 'posts'), 'post')
        pages = reader.read_files(os.path.join(self.dirname, 'pages'), 'page')
        self.assertEqual(posts[0].title, 'Post Title 2')
        self.assertEqual(pages[0].title, 'About me')

    def tearDown(self):
        teardown(self.dirname)

class ModelTests(unittest.TestCase):
    def setUp(self):
        self.dirname = setup_files()
        self.posts = reader.read_files(os.path.join(self.dirname, 'posts'), 'post')
        self.pages = reader.read_files(os.path.join(self.dirname, 'pages'), 'page')

    def test_post_pretty_date(self):
        self.assertEqual(self.posts[1].get_pretty_date(), 'July 01, 2015')

    def test_post_parse_filename(self):
        self.assertEqual(self.posts[1].slug, 'test-post')

    def tearDown(self):
        teardown(self.dirname)

if __name__ == '__main__':
    unittest.main()
