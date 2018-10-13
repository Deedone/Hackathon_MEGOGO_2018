import html_request
import urllib.request
import m3u8

class Search():

    def __init__(self):
        self.search("http://gidonline.in/?s=%D0%B1%D1%83&submit=%D0%9F%D0%BE%D0%B8%D1%81%D0%BA")

    def search(self, url):
        html_data = html_request.HTMLdata().get_img_tags(url)
        print(url)





#find = Search()


print('Beginning file download with urllib2...')

url = 'http://185.38.12.48/sec/1538779417/36343937bee6a5f558fb55e787e93eca087b91f42167faa7/ivs/30/8a/b03775386c24/480.mp4'  
urllib.request.urlretrieve(url, 'lol.mp4')  
