# nimbus

## quick start

```git clone https://github.com/pscohn/nimbus```
```cd nimbus/example```

Edit nimbus.ini to your liking:

    [default]
    site_title = Your Site Name
    author = Your Name
    domain = yourdomain.com
    email = your@email.com
    paginate_by = 5 #number of posts per page
    pages_path = /path/to/pages/directory
    posts_path = /path/to/posts/directory
    site_path = /path/to/site/target

    [menu]
    # place name/link pairs of the links you would like in the menu
    about = /about.html
    github = http://github.com/pscohn
    email = mailto:pscohn@gmail.com

###Creating Posts:

- Name file with this format in posts_path: YYYY-MM-DD-post-slug.html
- On first line: name of the post and a newline
- Beginning on second or third line: post content in Markdown

###Creating Pages:

- Name file anything you like in pages_path
- On first line: name of the page and a newline
- Beginning on second or third line: page content in Markdown

```python ../nimbus.py generate```
```python ../nimbus.py run```

## todos

- tests
- documentation
- og meta
- auto-regen when post updates
- refactor & more modular, user friendly
