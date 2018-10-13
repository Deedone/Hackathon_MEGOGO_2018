#!/usr/bin/env python3
import json
import sys
import urllib.request
import urllib.parse
import re
import logging
from html.parser import HTMLParser
 
 
def parse_frame(url, ref):
    request = urllib.request.Request(url, headers={'Referer': ref})
    response = urllib.request.urlopen(request)
    text = response.read().decode('utf-8')
    csrf_token = re.search(r"((?<=<meta name=\"csrf-token\" content=\")[^\"]*)", text).group(0)
    data_start_index = text.index("$.post(session_url")
    data_end_index = text.index("}).success", data_start_index)
    data_string = text[data_start_index:data_end_index]
    video_token = re.search(r"((?<=video_token: ')[^']*)", data_string).group(0)
    mw_key = re.search(r"((?<=mw_key: ')[^']*)", data_string).group(0)
    mw_pid = re.search(r"((?<=mw_pid: )[^,]*)", data_string).group(0)
    mw_domain_id = re.search(r"((?<=mw_domain_id: )[^,]*)", data_string).group(0)
    uuid = re.search(r"((?<=uuid: ')[^']*)", data_string).group(0)
    return parse_json(url, csrf_token, video_token, mw_key, mw_pid, mw_domain_id, uuid)
 
 
def parse_json(ref, csrf_token, video_token, mw_key, mw_pid, mw_domain_id, uuid):
    request = urllib.request.Request(
        'http://pandastream.cc/sessions/new_session',
        data=urllib.parse.urlencode({
            'video_token': video_token,
            'content_type': 'movie',
            'mw_key': mw_key,
            'mw_pid': mw_pid,
            'mw_domain_id': mw_domain_id,
            'ad_attr': '0',
            'debug': 'false',
            'uuid': uuid
        }).encode('ascii'),
        method='POST',
        headers={
            'Referer': ref,
            'X-Requested-With': 'XMLHttpRequest',
            'X-Iframe-Option': 'Direct',
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRF-Token': csrf_token
        }
 
    )
    response = urllib.request.urlopen(request)
    text2 = response.read().decode('utf-8')
    data = json.loads(text2)
    return data['mans']['manifest_m3u8']
 
 
def parse_page(url):
    class Parser(HTMLParser):
        def parse_html(self, html):
            self.feed(html)
            return self.result
 
        def error(self, message):
            logging.error(message)
 
        def __init__(self):
            super().__init__()
            self.result = None
 
        def handle_starttag(self, tag, attrs):
            attrs_d = dict((x, y) for x, y in attrs)
            if tag == 'iframe' and ('src' and 'class' in attrs_d) and attrs_d['class'] == 'ifram':
                self.result = parse_frame(attrs_d['src'], url)
 
    response = urllib.request.urlopen(url)
    return Parser().parse_html(response.read().decode('utf-8'))
 
 
def main(argc, argv):
    url = 'http://gidonline.club/2016/12/trolli/'
    if argc > 1:
        url = argv[1]
    result = parse_page(url)
    sys.stdout.write('%s\n' % result)
 
if __name__ == '__main__':
    main(len(sys.argv), sys.argv)
