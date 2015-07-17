class Post:
    def __init__(self, title, slug, date, body):
        self.title = title
        self.slug = slug
        self.body = body
        self.date = date

class Page:
    def __init__(self, title, body, path):
        self.title = title
        self.body = body
        self.path = path

