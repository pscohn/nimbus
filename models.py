class Post:
    def __init__(self, title, slug, date, body):
        self.title = title
        self.slug = slug
        self.body = body
        self.date = date

    def get_pretty_date(self):
        return self.date.strftime('%B %d, %Y')

class Page:
    def __init__(self, title, body, path):
        self.title = title
        self.body = body
        self.path = path
