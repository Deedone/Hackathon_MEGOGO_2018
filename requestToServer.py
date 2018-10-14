import m3u8
import requests
"""
m3u8_obj = m3u8.load('http://185.38.12.56/sec/1538873092/33333831c70b51f2748d885bccb6eed4c1cde5e28dcb6577/ivs/d2/ce/0afaf251ffe8.mp4/hls/tracks-1,4/index.m3u8') # this could also be an absolute filename
print (m3u8_obj.segments)
print (m3u8_obj.target_duration)

#m3u8_obj = m3u8.loads('#EXTM3U8 ... etc ... ')
playlist=[el['uri'] for el in m3u8_obj.data['segments']]
print(playlist)

 
 """
# Запрос 1 на сайт для получения доступа к файлу, в котором идет ссылка на поток
# если ответ "success"
# тогда запрос удачен, иначе не удачен 
#
#
class RequestToSearch:

    def post(string):
        headers = {            
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Length': '140',
            'Content-Type': 'application/x-www-form-urlencoded',
            'DNT': '1',
            'Host': 'baskino.me',
            'Origin': 'http://baskino.me',
            'Referer': 'http://baskino.me/index.php?do=search',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
        }
        data = {
            'do': 'search',
            'subaction': 'search',
            'actors_only': '0',
            'search_start': '0',
            'full_search': '0',
            'result_from': '1',
            'result_from': '1',
            'story': string
            }


        r = requests.post('http://baskino.me/index.php?do=search', headers=headers, data=data)
        return r

