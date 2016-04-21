#!/usr/bin/python
#coding=utf-8
#
#
# Copyright (c) 2016 fusijie <fusijie@vip.qq.com>
#
# MIT Licence. See http://opensource.org/licenses/MIT
#
# Created on 2016-04-20
#

import sys
import os
import re
from workflow import Workflow, web

lastest_url = 'http://news-at.zhihu.com/api/2/news/latest'
default_zhihu_homepage = 'http://daily.zhihu.com/'
default_thumsnail = 'icon.png'

def _get_stories_url():
    stories_url = lastest_url
    return stories_url

def _parse_stories():
    data = web.get(_get_stories_url()).json()
    return data

def _get_story_icon_file_path(wf, dir, img_url):
    regex = r'\w+\.\w+$'
    match = re.search(regex, img_url)
    img_name = match.group(0)
    img_cache_full_path = wf.cachedir + '/thumbnail_cache/' + dir + '/' + img_name
    if not os.path.exists(img_cache_full_path):
        web.get(img_url).save_to_path(img_cache_full_path)
    if not os.path.exists(img_cache_full_path):
        return default_thumsnail
    else:
        return img_cache_full_path

def _get_stories(wf):
    data = wf.cached_data('zhihu_lastest', _parse_stories, max_age = 30)
    stories = data['news']
    stories_date = data['date']
    for story in stories:
        story_title = story['title']
        story_url = story['share_url']
        story_thumbnail = story['thumbnail']
        wf.add_item(title = story_title, subtitle = story_url, icon = _get_story_icon_file_path(wf, stories_date, story_thumbnail), arg = story_url, valid = True)
    wf.send_feedback()

def main(wf):
    try:
        _get_stories(wf)
    except:
        pass

if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(main))