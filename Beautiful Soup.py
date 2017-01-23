# -*- coding:utf-8 -*-

import urllib2
from bs4 import BeautifulSoup

# broken_html = '<ul class=country><li>Area<li>Population</ul>'
# soup = BeautifulSoup(broken_html, 'html.parser')
# fixed_html = soup.prettify()
# ul = soup.find('ul', attrs={'class':'country'})
# print ul.find_all('li')



# def download(url, user_agent = 'wswp', proxy = None, num_retries = 2):
#     print 'Downloading:', url
#     headers = {'User-agent': user_agent}
#     request = urllib2.Request(url, headers=headers)
#
#     opener = urllib2.build_opener()
#     if proxy:
#         proxy_params = {urlparse.urlparse(url).scheme: proxy}
#         opener.add_handler(urllib2.ProxyHandler(proxy_params))
#     try:
#         html = opener.open(request).read()
#     except urllib2.URLError as e:
#         print 'Download error:', e.reason
#         html = None
#         if num_retries > 0:
#             if hasattr(e, 'code') and 500 <= e.code < 600:
#                 html = download(url, user_agent, proxy, num_retries-1)
#     return html


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



url = 'http://example.webscraping.com/places/view/United-Kingdom-239'
html = download(url)
# print html
soup = BeautifulSoup(html)
# print soup
tr = soup.find(attrs={'id':'places_area__row'})
#print tr
td = tr.find(attrs={'class':'w2p_fw'})
area = td.text
print area       #DONE