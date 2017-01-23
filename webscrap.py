# -*- coding:utf-8 -*-

import urllib2

def download1(url):
    return urllib2.urlopen(url).read()






def download2(url):
    print 'Downloading:', url
    try:
        html = urllib2.urlopen(url).read()
    except urllib2.URLError as e:
        print 'Download error:', e.reason
        html = None
    return html






def download3(url, num_retries = 2):      #重试两次
    print 'Dowloading:', url
    try:
        html = urllib2.urlopen(url).read()
    except urllib2.URLError as e:
        print 'Download error:', e.reason
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                #recursively retry 5xx HTTP errors
                return download(url, num_retries-1)
    return html

# print download('http://example.webscraping.com')
#print download('http://www.meetup.com')         #FAILE




def download4(url, user_agent = 'wswp', num_retries = 2):
    print 'Downloading:', url
    headers = {'User-agent': user_agent}
    request = urllib2.Request(url, headers = headers)
    try:
        html = urllib2.urlopen(request).read()
    except urllib2.URLError as e:
        print 'Download error:', e.reason
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                # retry 5xx HTTP errors
                return download(url, user_agent, num_retries-1)
    return html

# print download('http://www.meetup.com')  #DONE

#proxy

# proxy = ...
# opener = urllib2.build_opener()
# proxy_params = {urlparse.urlparse(url).scheme: proxy}
# opener.add_handler(urllib2.ProxyHandler(proxy_params))
# response = opener.open(request)

def download(url, user_agent = 'wswp', proxy = None, num_retries = 2):         #增添代理
    print 'Downloading:', url
    headers = {'User-agent': user_agent}
    request = urllib2.Request(url, headers=headers)

    opener = urllib2.build_opener()
    if proxy:
        proxy_params = {urlparse.urlparse(url).scheme: proxy}
        opener.add_handler(urllib2.ProxyHandler(proxy_params))
    try:
        html = opener.open(request).read()
    except urllib2.URLError as e:
        print 'Download error:', e.reason
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                html = download(url, user_agent, proxy, num_retries-1)
    return html


import re

def crawl_sitemap(url):
    # download the sitemap file
    sitemap = download(url)
    # extract the sitemap links
    links = re.findall('<loc>(.*?)</loc>', sitemap)
    # download each link
    for link in links:
        html = download(link)

#print crawl_sitemap('http://example.webscraping.com/sitemap.xml')



import itertools

# maximum number of consecutive download errors allowed
max_errors = 5
# # current number of consecutive download errors
num_errors = 0

# for page in itertools.count(1):
#     url = 'http://example.webscraping.com/view/-%d' % page
#     html = download(url)
#     if html is None:
#         #received an error trying to download this webpage
#         num_errors += 1
#         if num_errors == max_errors:
#             break
#     else:
#         num_errors = 0

def link_crawler1(seed_url, link_regex):
    crawl_queue = [seed_url]
    while crawl_queue:
        url = crawl_queue.pop()
        html = download(url)
        for link in get_links(html):
            if re.match(link_regex, link):
                crawl_queue.append(link)

def get_links(html):
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    return webpage_regex.findall(html)



import urlparse
def link_crawler2(seed_url, link_regex):
    crawl_queue = [seed_url]
    while crawl_queue:
        url = crawl_queue.pop()
        html = download(url)
        for link in get_links(html):
            if re.match(link_regex, link):
                link = urlparse.urljoin(seed_url, link)
                crawl_queue.append(link)


import robotparser
rp = robotparser.RobotFileParser()
rp.set_url('http://example.webscraping.com/robots.txt')
rp.read()

user_agent = 'wswp'

def link_crawler(seed_url, link_regex):
    crawl_queue = [seed_url]
    seen = set(crawl_queue)
    while crawl_queue:
        url = crawl_queue.pop()
        if rp.can_fetch(user_agent, url):
            html = download(url)
            for link in get_links(html):
                if re.match(link_regex, link):
                    link = urlparse.urljoin(seed_url, link)
                    if link not in seen:
                        seen.add(link)
                        crawl_queue.append(link)
        else:
            print 'Blocked by robots.txt:', url

class Throttle:                   #记录每个域名上次访问的时间
    def __init__(self, delay):
        # amount of delay between downloads for each domain
        self.delay = delay
        # timestamp of when a domain was last accessed
        self.domains = {}

def wait(self, url):
    domain = urlparse.urlparse(url).netloc
    last_accessed = self.domains.get(domain)

    if self.delay > 0 and last_accessed is not None:
        sleep_secs = self.delay - (datetime.datetime.now() - last_accessed).seconds
        if sleep_secs > 0:
            # domain has been accessed recently
            # so need to sleep
            time.sleep(sleep_secs)
    # update the last accessed time
    self.domains[domain] = datetime.datetime.now()



if __name__ == '__main__':
    link_crawler('http://example.webscraping.com', '/(index|view)')


