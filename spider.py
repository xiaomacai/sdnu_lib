# coding: utf-8
"""
页面分析及爬虫
"""
import requests
import json
from db_opt import DateOpt
from datetime import datetime

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
    'date': datetime.now().strftime('%Y-%m-%d'),
    'fr_start': '',
    'fr_end': '',
    'act': 'get_rsv_sta',
    '_': ''
}

r = requests.get(url, headers=headers, data=data)
res = json.loads(r.content)
for item in res['data']:
    # DateOpt().insert_into_desk(item['name'])

    if item['name'][1] == 'F' and item['ts']:
        for item2 in item['ts']:
            if item2['state'] == 'doing':
                desk_name = item['name']
                student_name = item2['owner']
                student_card_id = item2['accno']
                start = item2['start'][-5:]
                end = item2['end'][-5:]

                desk_id = DateOpt().select_id_from_desk(desk_name)
                if not desk_id:
                    desk_id = DateOpt().select_id_from_desk(desk_name)
                student_id = DateOpt().select_id_from_student(student_name, student_card_id)
                if not student_id:
                    student_id = DateOpt().select_id_from_student(student_name, student_card_id)
                # print(desk_id, student_id)
                DateOpt().update_occupy(desk_id, student_id, start, end)
                # DateOpt().insert_into_student(item2['owner'], item2['accno'])
