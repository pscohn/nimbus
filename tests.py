import unittest
import datetime
import random
import shutil
import os

import models

class ReaderTests(unittest.TestCase):
    def setUp(self):
        self.dirname = 'nimbustest-' + str(random.randrange(1000, 10000000))
        os.mkdir(self.dirname)

    def test_read(self):
        shutil.rmtree(self.dirname)

class ModelTests(unittest.TestCase):
    def test_page(self):
        p = models.Page(title='Title', body='Body', path='page.html')
        self.assertEqual(p.title, 'Title')
        self.assertEqual(p.body, 'Body')
        self.assertEqual(p.path, 'page.html')

    def test_post(self):
        p = models.Post(title='Title',
                        body='Body',
                        slug='slug',
                        date=datetime.date(2015, 7, 1))                        
        self.assertEqual(p.title, 'Title')
        self.assertEqual(p.body, 'Body')
        self.assertEqual(p.slug, 'slug')
        self.assertEqual(p.get_pretty_date(), 'July 01, 2015')

if __name__ == '__main__':
    unittest.main()
