# -*- coding: utf-8 -*-

import urllib2
import lxml.html

def download(url, user_agent=None):
    print 'Downloading:', url
    headers = {'User-agent':user_agent or 'wswp'}
    request = urllib2.Request(url, headers = headers)
    try:
        html = urllib2.urlopen(request).read()
    except urllib2.URLError as e:
        print 'Download error:', e.reason
        html = None
    return html

def scrape(html):
    tree = lxml.html.fromstring(html)
    td = tree.cssselect('tr#places_area__row > td.w2p_fw')[0]
    area = td.text_content()
    return area

# broken_html = '<ul class=country><li>Area<li>Population</ul>'
# tree = lxml.html.fromstring(broken_html)
# fixed_html = lxml.html.tostring(tree, pretty_print=True)
# print fixed_html


if __name__ == '__main__':
    html = urllib2.urlopen('http://example.webscraping.com/view/United-Kingdom-239').read()
    print scrape(html)