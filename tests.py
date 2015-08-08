import unittest
import datetime
import random
import shutil
import os

import models
import reader

exampleposts = [
    ('2015-07-01-test-post.md', 'Post Title\n\nPostBody'),
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
    pass
    #shutil.rmtree(dirname)

class ReaderTests(unittest.TestCase):
    def setUp(self):
        self.dirname = setup_files()

    def test_read(self):
        folder = os.path.join(self.dirname, 'posts')
        filenames, filebodys = reader._read(folder)
        self.assertEqual(len(exampleposts), len(filenames))
        self.assertEqual(filenames[0], exampleposts[0][0])

    def tearDown(self):
        teardown(self.dirname)

class ModelTests(unittest.TestCase):
    def test_page(self):
        pass
        #p = models.Page()

    def test_post(self):
        pass
        #p = models.Post()
        #self.assertEqual(p.get_pretty_date(), 'July 01, 2015')

if __name__ == '__main__':
    unittest.main()
