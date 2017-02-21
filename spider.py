# coding: utf-8
"""
页面分析及爬虫
"""
import requests
import json
from db_opt import DateOpt

url = 'http://210.44.14.49/ClientWeb/pro/ajax/device.aspx'

headers = {
    'Host': '210.44.14.49',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Sa'
                  'fari/537.36',
}

data = {
    'byType': 'devcls',
    'classkind': '',
    'display': 'fp',
    'md': 'd',
    'room_id': '',
    'purpose': '',
    'img': '',
    'cld_name': 'default',
    'date': '2017-02-20',
    'fr_start': '',
    'fr_end': '',
    'act': 'get_rsv_sta',
    '_': ''
}

r = requests.get(url, headers=headers, data=data)
res = json.loads(r.content)
for item in res['data']:
    if item['name'][1] == 'F' and item['ts']:
        if item['ts'][0]['state'] != 'doing':
            print item['name'], item['ts']
