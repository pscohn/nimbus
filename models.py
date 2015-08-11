import datetime
import markdown
import math

CATEGORIES = {}

class Paginator:
    def __init__(self, file_base, posts, paginate_by):
        self.file_base = file_base
        self.posts = posts
        self.paginate_by = paginate_by
        self.max_pages = math.ceil(len(self.posts) / self.paginate_by)
        self.cursor = 1

    def pages(self):
        while self.cursor <= self.max_pages:
            yield self
            self.cursor += 1

    def page(self):
        return self.posts[(self.cursor-1)*self.paginate_by:self.cursor*self.paginate_by]

    def has_previous(self):
        return self.cursor >= 1

    def has_next(self):
        return self.cursor < self.max_pages

    def current_page(self):
        if self.cursor == 1:
            return self.file_base + '.html'

        return '%s_%s.html' % (self.file_base, self.cursor)

    def previous_page(self):
        if self.cursor <= 2:
            return self.file_base + '.html' 

        return '%s_%s.html' % (self.file_base, self.cursor - 1)
        
    def next_page(self):
        if not self.has_next():
            return '%s_%s.html' % (self.file_base, self.cursor)

        return '%s_%s.html' % (self.file_base, self.cursor + 1)

class StaticFile(object):
    """Base class for Post and Page objects."""

    def __init__(self, filename, filebody):
        self._filename = filename
        self._filebody = filebody
        self._parse()

    def _parse(self):
        self._parse_filename()
        self._parse_content()

    def _parse_filename():
        pass

    def _parse_content(self):
        split = self._filebody.split('\n')
        self.title = split[0].strip()
        self.body = markdown.markdown('\n'.join(split[1:]).strip())

class Post(StaticFile):
    def __init__(self, *args):
        self.title = None
        self.slug = None
        self.body = None
        self.date = None
        self.categories = None
        super().__init__(*args)

    def get_pretty_date(self):
        return self.date.strftime('%B %d, %Y')

    def _parse_filename(self):
        split = self._filename.split('-')
        self.slug = '-'.join(split[3:])[:-3] # strip .md from end

        year, month, day = split[:3]
        self.date = datetime.date(int(year), int(month), int(day))

    def _parse_content(self):
        split = self._filebody.split('\n')
        self.title = split[0].strip()
        self.body = split[1:]
        if self.body[0].strip().startswith('categories:'):
            categories = self.body[0]
            self.body = '\n'.join(self.body[1:])
            self.categories = categories[11:].strip().split(', ')
            for category in self.categories:
                if category in CATEGORIES:
                    CATEGORIES[category].append(self)
                else:
                    CATEGORIES[category] = [self]
        else:
            self.body = '\n'.join(self.body)

class Page(StaticFile):
    def __init__(self, *args):
        self.title = None
        self.body = None
        self.path = None
        super().__init__(*args)

    def _parse_filename(self):
        self.path = self._filename[:-3] + '.html' # replace .md with .html
