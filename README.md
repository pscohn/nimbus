# nimbus

Nimbus is a simple static blog generator that supports posts and pages using Markdown, pagination, and RSS.

## quick start

```git clone https://github.com/pscohn/nimbus```

```cd nimbus/example```

Nimbus looks in the current directory for a nimbus.ini to generate the site with your settings, but you may move the example folder to any location and update the paths accordingly in the nimbus.ini.

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
- Beginning on second or later: post content in Markdown

###Creating Pages:

- Name file anything you like in pages_path
- On first line: name of the page and a newline
- Beginning on second or later: page content in Markdown

###Generate and Run Dev Server

```python ../nimbus.py generate```

```python ../nimbus.py run```

And visit http://127.0.0.1:8080 to view your site.

**Warning**: the generate command will overwrite files in the site_path directory with the same name as index.html, any files in pages_path, and will create/overwrite the site_path/posts directory.

## todos

- categories
- tests
- documentation
- og meta
- auto-regen when post updates
- refactor & more modular, user friendly
