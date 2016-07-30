#-*- coding: utf-8 -*-
#!/usr/bin/env python
import os
import logging

from flask import Flask
from flask import render_template
from flask import request

from models import TagText
from crawler import Crawler

DEBUG = os.getenv('SERVER_SOFTWARE', '').startswith('Development/')
CRAWL_TAGS_COUNT = DEBUG and 5 or 10

app = Flask(__name__)
crawler = Crawler()

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/crawl')
def crawl():
  tags = TagText.sample_last_tags(CRAWL_TAGS_COUNT)
  media = crawler.run(tags)
  count = TagText.save(media)
  results = 'Count: %s, %d' % (' '.join(tags), count)
  logging.info(results)
  return results

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404

@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500
