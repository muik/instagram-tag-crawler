#-*- coding: utf-8 -*-
import logging
import random
import re

from google.appengine.ext import ndb
from google.appengine.api import memcache

class TagText_Sampling(ndb.Model):
  MAX_CODES_COUNT = 300
  MAX_OWNER_COUNT = 300
  KEY_RECENT_CODES = 'recent_codes'
  KEY_PRE_OWNER_IDS = 'pre_owner_ids'

  # use TextProperty for not exceeding free quota
  codes_inline = ndb.TextProperty()
  text = ndb.TextProperty()
  created_at = ndb.DateTimeProperty(auto_now_add=True)

  @classmethod
  def _get_recent_codes(cls):
    inline = memcache.get(cls.KEY_RECENT_CODES)
    if inline == None:
      tag_text = cls.query().order(-cls.created_at).get()
      return tag_text and tag_text.codes_inline and tag_text.codes_inline.split() or []
    return inline.split()

  @classmethod
  def save(cls, media):
    recent_owner_ids = (memcache.get(cls.KEY_PRE_OWNER_IDS) or '').split()
    recent_codes = cls._get_recent_codes()
    codes_set = set(recent_codes)
    owner_ids_set = set(recent_owner_ids)
    new_media = []

    for item in media:
      if not TagValidator.is_valid_tags(item['tags']):
        continue
      if item['code'] in codes_set:
        continue
      if item['owner']['id'] in owner_ids_set:
        continue
      new_media.append(item)
      owner_ids_set.add(item['owner']['id'])
      codes_set.add(item['code'])

    if not new_media:
      return 0

    tag_text = cls()
    tag_text.codes_inline = ' '.join([x['code'] for x in new_media])
    tag_text.text = '\n'.join([' '.join(x['tags']) for x in new_media])
    tag_text.put()

    recent_codes.extend([x['code'] for x in media])
    recent_owner_ids.extend([x['owner']['id'] for x in new_media])
    cls._set_cache(recent_codes, cls.MAX_CODES_COUNT, cls.KEY_RECENT_CODES)
    cls._set_cache(recent_owner_ids, cls.MAX_OWNER_COUNT, cls.KEY_PRE_OWNER_IDS)

    tags = reduce(lambda y,x: y+x['tags'], new_media, [])
    tags = set(tags)
    cls._set_last_tags(tags)

    return len(new_media)

  DEFAULT_TAGS = [u'맛집', u'먹스타그램', u'일상', u'인스타그램', u'여행스타그램']

  @classmethod
  def sample_last_tags(cls, count):
    tags = cls._last_tags()
    tags = [tag for tag in tags if re.search(u'[ㄱ-ㅎㅏ-ㅣ가-힣]', tag)]
    if len(tags) < count:
      return cls.DEFAULT_TAGS
    return random.sample(tags, count)

  @classmethod
  def _last_tags(cls):
    last_tags_inline = memcache.get('tag_text_last_tags') or ''
    return last_tags_inline.split()

  @classmethod
  def _set_last_tags(cls, tags):
    memcache.set('tag_text_last_tags', ' '.join(tags))

  @classmethod
  def _set_cache(cls, items, max_cnt, key):
    cnt = len(items)
    if cnt > max_cnt:
      items = items[cnt - max_cnt:]
    memcache.set(key, ' '.join(items))

# for model clustering
TagText = TagText_Sampling


class TagValidator:
  MIN_TAGS_COUNT = 3
  BAD_TAGS = set([u'섹스',u'섹그램',u'섹텍',u'야그램',u'가슴',u'슴스타그램',
      u'일탈',u'일탈남',u'일탈녀',u'여자신음',u'오프녀',u'19금',u'가슴노출',
      u'섹스녀',u'섹파구함',u'섹스싸이트',u'일수',u'성형대출',u'조건만남'])

  @classmethod
  def is_valid_tags(cls, tags):
    if not tags or len(tags) < cls.MIN_TAGS_COUNT:
      return False
    return cls.BAD_TAGS.isdisjoint(tags)

