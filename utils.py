import os

def fread(path):
    f = open(path)
    content = f.read()
    f.close()
    return content

def remove_existing(path):
    for post in os.listdir(path):
        os.remove(os.path.join(path, post))

def printnum(num, noun):
    if num == 1:
        print('generated 1 %s' % noun)
    else:
        print('generated %s %ss' % (num, noun))
