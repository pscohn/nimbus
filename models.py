import datetime
import markdown

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
        super().__init__(*args)

    def get_pretty_date(self):
        return self.date.strftime('%B %d, %Y')

    def _parse_filename(self):
        split = self._filename.split('-')
        self.slug = '-'.join(split[3:])[:-3] # strip .html from end

        year, month, day = split[:3]
        self.date = datetime.date(int(year), int(month), int(day))

class Page(StaticFile):
    def __init__(self, *args):
        self.title = None
        self.body = None
        self.path = None
        super().__init__(*args)

    def _parse_filename(self):
        self.path = self._filename[:-3] + '.html' # replace .md with .html




