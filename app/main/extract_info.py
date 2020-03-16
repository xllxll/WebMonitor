import re

import feedparser
from func_timeout import func_set_timeout

from app.main.selector.selector_handler import new_handler
from config import logger


def extract_by_re(conetnt, regular_expression):
    m = re.search(regular_expression, conetnt)

    if m:
        return m.groups()[0]
    else:
        logger.error('{} 无法使用正则提取'.format(regular_expression))
        raise Exception('无法使用正则提取')


def get_content(url,
                is_chrome,
                selector_type,
                selector,
                regular_expression=None,
                headers=None,
                debug=False):
    if is_chrome == 'no':
        selector_handler = new_handler('request', debug)
    else:
        selector_handler = new_handler('phantomjs', debug)

    if selector_type == 'xpath':
        content = selector_handler.get_by_xpath(url, selector, headers)
    elif selector_type == 'css':
        content = selector_handler.get_by_css(url, selector, headers)
    elif selector_type == 'json':
        content = selector_handler.get_by_json(url, selector, headers)
    else:
        logger.error('无效选择器')
        raise Exception('无效选择器')

    if regular_expression:
        content = extract_by_re(content, regular_expression)
    return content


@func_set_timeout(5)
def get_rss_content(url):
    feeds = feedparser.parse(url)

    if len(feeds.entries) == 0:
        raise Exception('无内容')

    single_post = feeds.entries[0]
    item = {}
    item['title'] = single_post.title
    item['link'] = single_post.link
    item['guid'] = single_post.id

    return item
