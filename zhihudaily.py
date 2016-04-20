#!/usr/bin/python
#coding=utf-8

import sys
from workflow import Workflow, ICON_WEB, web

lastest_url = 'http://news-at.zhihu.com/api/4/news/latest'
theme_url = 'http://news-at.zhihu.com/api/4/theme/'

detail_url_prefix ='http://news-at.zhihu.com/api/4/news/'
default_zhihu_homepage = 'http://daily.zhihu.com/'

def _get_stories_url():
    stories_url = lastest_url
    if category_index == 999: #lastest
        stories_url = lastest_url
    else: #theme
        stories_url = theme_url + str(category_index)
    return stories_url

def _parse_stories():
    data = web.get(_get_stories_url()).json()
    stories = data['stories']
    for story in stories:
        story_title = story['title']
        story_fake_url = detail_url_prefix + str(story['id'])
        story_data = web.get(story_fake_url).json()
        if 'share_url' in story_data:
            story_real_url = story_data['share_url']
            story['real_url'] = story_real_url
        else:
            story['real_url'] = default_zhihu_homepage
    return data

def _get_stories(wf):
    data = wf.cached_data('zhihu_' + str(category_index), _parse_stories, max_age = 30)
    stories = data['stories']
    for story in stories:
        story_title = story['title']
        story_url = story['real_url']
        wf.add_item(title = story_title, subtitle = story_url, icon = 'icon.png', arg = story_url, valid = True)
    wf.send_feedback()


def main(wf):
    global category_index
    # category_index = sys.argv[1]
    category_index = 999
    _get_stories(wf)

if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(main))