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
headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'Content-Length': '82',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'DNT': '1',
    'Host': 'ampatcape.com',
    'Origin': 'http://ampatcape.com',
    'Referer': 'http://ampatcape.com/video/b953c40ea738e66d/iframe?nocontrols=1&season=&episode=&ref=all1NnlGb0diUFo2dmNzaUlTYjZYcEF2bENkUDUwbnBabGtRN1prN20rVlY5M0lnNDZSR2xQTjIycEUya2pSWXZTUzQzWG5kcTlCV2VHM0ZlVko2SlBIYmtUTkVRaTNPT25RSG9ZM2N2SzREZUsyaVNpRm16Z3RqV3BGVzE2ZkpYc0ZSZDRoV0c5dVRRa2I4S216RjJyem5NSTJIL2FuQlN5U2pEZDN3Z0pJQU4rWHl2dHZMdnhQekxnVHJmMnk2LS1UOW9GL293d1JXbzNyL2VWSlZvWkVnPT0=--22c15de58bd9e09dd615f19608d4bff3c4b59e78',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}
data = {
    'name': 'click',
    'vast_null': 'false',
    'adb': 'false',
    'domain_id': '455914',
    'video_token': 'b953c40ea738e66d'
}


r = requests.post('http://ampatcape.com/stats/event', headers=headers, data=data)
print(r.connection)
print(r.headers)
print(r.cookies)
print(r.content)
print(r.text)

# Запрос 2 на сайт для получения доступа к файлу, в котором идет ссылка на поток
# если ответ ссылка "....."
# тогда запрос удачен, иначе не удачен 
#
#

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'Content-Length': '258',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'DNT': '1',
    'Host': 'ampatcape.com',
    'Origin': 'http://ampatcape.com',
    'Referer': 'http://ampatcape.com/video/b953c40ea738e66d/iframe?nocontrols=1&season=&episode=&ref=all1NnlGb0diUFo2dmNzaUlTYjZYcEF2bENkUDUwbnBabGtRN1prN20rVlY5M0lnNDZSR2xQTjIycEUya2pSWXZTUzQzWG5kcTlCV2VHM0ZlVko2SlBIYmtUTkVRaTNPT25RSG9ZM2N2SzREZUsyaVNpRm16Z3RqV3BGVzE2ZkpYc0ZSZDRoV0c5dVRRa2I4S216RjJyem5NSTJIL2FuQlN5U2pEZDN3Z0pJQU4rWHl2dHZMdnhQekxnVHJmMnk2LS1UOW9GL293d1JXbzNyL2VWSlZvWkVnPT0=--22c15de58bd9e09dd615f19608d4bff3c4b59e78',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}
data = {
  'q' : 'b953c40ea738e66d'
  }
         
  #m3u8: "http://ampatcape.com/manifest/index.m3u8?tok=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzb3VyY2UiOiJzZXNzaW9uIiwiZXhwIjoxNTM4ODU1MjcxLCJ2IjoiYjk1M2M0MGVhNzM4ZTY2ZCIsImEiOmZhbHNlLCJwIjo0Nzg3LCJoIjoiZmE3NTQ4MDlmYzNlMmZlNDQwYjc0NDljNDdkNzQyNzRmYzdkZjgzMzUyNDMwMmIyMTNjMjI1NGNkMDY4MTk1NCJ9.VhF1woHCHE1muFLtINuumtVO5BHoZDU3RTPCFo0dN4Y

r1 = requests.post('http://ampatcape.com/vs', headers=headers, data=data)
print(r1.content)
print(r1.text)



"""
e.parse_query_string = function(e) {
        var t = e.match(/\?(.*)/);
        if (t && t[1]) {
            for (var i = t[1].split("&"), n = {}, r = 0; r < i.length; r++) {
                var a = i[r].split("=");
                if (void 0 === n[a[0]])
                    n[a[0]] = decodeURIComponent(a[1]);
                else if ("string" == typeof n[a[0]]) {
                    var o = [n[a[0]], decodeURIComponent(a[1])];
                    n[a[0]] = o
                } else
                    n[a[0]].push(decodeURIComponent(a[1]))
            }
            return n
        }
        return []
    }
    """
