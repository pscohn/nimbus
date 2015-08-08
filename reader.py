import os

from models import *

def _read(folder):
    filenames = []
    contents = []
    for filename in os.listdir(folder):
        if len(filename) < 4:
            continue

        if filename[0] != '.' and filename[-3:] == '.md' and filename != 'index.md':
            filenames.append(filename)
            with open('%s/' % folder + filename) as f:
                contents.append(f.read())

    return filenames, contents

def read_files(path, filetype):
    filenames, filebodys = _read(path)
    file_objects = []

    if filetype == 'post':
        for i, filebody in enumerate(filebodys):
            file_objects.append(Post(filenames[i], filebody))
            return file_objects[::-1] # return posts in reverse order

    elif filetype == 'page':
        for i, filebody in enumerate(filebodys):
            file_objects.append(Post(filenames[i], filebody))
            return file_objects

