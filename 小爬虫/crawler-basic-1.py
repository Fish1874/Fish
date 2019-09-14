import requests
from lxml import etree

'''
如果不添加cookie，则返回回来的内容不会显示
'''

headers= {
    'User-Agent': 'Mozilla/5.0(Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36 LBBROWSER',
    'cookie' : '_ga=GA1.2.1550718085.1568266595; _gid=GA1.2.1397303275.1568266595; footprints=eyJpdiI6Ik96MkRiM3duWk9adEJJZUhDaGJKYXc9PSIsInZhbHVlIjoid0dSbUNaN1FYT2RDelB5R1dyY3ZGUUlzMGhZS0I3WnVVOFMrSFBWcDV3YVV0Z0tLZzFpRERleWFFT2pndTJzUCIsIm1hYyI6IjkyZTRkMmI5OTA5MGNkZTJkODhhNDI0OGQ0N2Q3MDRjNWE5Mjk2OGM4NzA3N2QxZWM4NGFiM2FiY2MxN2Q2OTIifQ%3D%3D; Hm_lvt_020fbaad6104bcddd1db12d6b78812f6=1568266595,1568266657; XSRF-TOKEN=eyJpdiI6IkVDaVJXUzl1XC9XazZHR2dEZnNZMXBRPT0iLCJ2YWx1ZSI6IlpsQ3hxU1IzbWJBd3o2SVdXM2U0ODdaVUF6TUhSem9TM04wNEMrSzRtUHN4XC9nd3ExMjVtODlpaVNSbHVTUERwIiwibWFjIjoiMzA3NmVlMzFkODc4NjUzYzcyNDlmOTMyMTY1NjU1MDEyYzFhNzI1YTZkMGM5YTBiMGNmMzI4ZTU2NDg5NjE1ZCJ9; glidedsky_session=eyJpdiI6Ik1cL3NWdFwvQ1JlVG9oczVsWnBOZVRrdz09IiwidmFsdWUiOiJNRG1URVwvbEd3OHc4V3E1XC9DbDNndm9MZ1JDdk40NVhPdWozT0N3YVJSSXZTMUtMOXpDSVJcL2RaODJvTDFcL3BUVSIsIm1hYyI6Ijc1MTE1NzlkMzhlZDZlNWI2NTlmNGM2MGYzNTM5ZjU4ZDk2OGFhOWQyZWU4NjZhZDBiODhkYzQ1MDJkYjFjYjcifQ%3D%3D; Hm_lpvt_020fbaad6104bcddd1db12d6b78812f6=1568269608',
    }
url = 'http://glidedsky.com/level/web/crawler-basic-1'

response = requests.get(url,headers=headers).text

html = etree.HTML(response)
content = html.xpath('//*/div[@class="col-md-1"]/text()')
sum = 0
for i in content:
    a = i.strip()
    sum += int(a)
print(sum)