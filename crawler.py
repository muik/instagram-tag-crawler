#-*- coding: utf-8 -*-
import re
import time
import json
import logging

from google.appengine.api import urlfetch

class Crawler:
  def __init__(self):
    pass
    
  def run(self, tags):
    rpc_list = [urlfetch.create_rpc() for x in xrange(len(tags))]
    for rpc, tag in zip(rpc_list, tags):
      self._fetch_async(rpc, tag)
      time.sleep(0.5) # prevent to be blocked
    return reduce(lambda s,rpc: s + self._parse_result(rpc.get_result()),
        rpc_list, [])

  def _fetch_async(self, rpc, tag):
    url = 'https://www.instagram.com/explore/tags/%s/' % tag
    return urlfetch.make_fetch_call(rpc, url)

  def _parse_result(self, result):
    if result.status_code == 404:
      logging.warning('Not found tag page')
      return []
    if result.status_code != 200:
      raise Exception('Invalid status code: %d' % result.status_code)
    return self._parse(result.content)

  def _parse(self, content):
    s = content.index('{"country_code":')
    e = content.index(';</script>', s)
    dumps = content[s:e]
    obj = json.loads(dumps)
    nodes = obj['entry_data']['TagPage'][0]['tag']['media']['nodes']
    for node in nodes:
      if 'caption' in node:
        node['tags'] = self._get_tags(node['caption'])
      else:
        node['tags'] = []
    return nodes

  def _get_tags(self, caption):
    return [x[1:] for x in re.findall(r'#[^#\s\',\(\)!\.~\-/&\+\*$]+', caption)]

