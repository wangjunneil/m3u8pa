import urllib.parse
import requests
import json
import random

user_agents = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3795.0 Safari/537.36',
    'Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Windows Phone 10.0; Android 6.0.1; Microsoft; RM-1152) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Mobile Safari/537.36 Edge/15.15254',
    'Mozilla/5.0 (Linux; Android 7.0; Pixel C Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.98 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1'
]

common_headers = {
    'Accept': 'application/json, text/javascript, */*',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'User-Agent': user_agents[random.randint(0, len(user_agents) - 1)],
    'Cache-Control': 'no-cache',
    'accept-encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'cache-control': "no-cache"
}

def simple(url):
    common_headers['Host'] = 'jx.a0296.cn'
    common_headers['Refer'] = 'http://y.mt2t.com/lines?url=' + urllib.parse.quote(url)

    payload = { "url": url, "lg": "" }
    response = requests.post('http://jx.a0296.cn/api.php', data=payload, headers=common_headers)
    result = response.json()
    print(result)
    if result['code'] == '500':
        raise Exception(result['msg'])
    return [result['url']]

def multiple(url):
    common_headers['Host'] = 'y.mt2t.com'

    payload = { "url": url }
    response = requests.post('http://y.mt2t.com/lines/getdata', data=payload, headers=common_headers)
    m3u8_list = response.json();
    print(m3u8_list)

    m3u8List = []
    for e in m3u8_list:
        str = e['Url'].replace('http://y2.mt2t.com:91/ifr?url=', '').replace('&type=m3u8','')
        base64Str = urllib.parse.unquote(str)
        
        common_headers['Host'] = 'y2.mt2t.com:91'
        payload = { "url": base64Str }
        response = requests.post('http://y2.mt2t.com:91/ifr/api', data=payload, headers=common_headers)
        result = response.json();
        print(result)

        if result['msg'] == 'ok' and len(result['url']) != 0:
            m3u8List.append(result['url'])

    return list(set(m3u8List))

def aggregation(url):
    m3u8s = multiple(url)
    m3u8s = m3u8s + simple(url)
    return m3u8s