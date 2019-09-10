# 登录知乎后抓取你的知乎时间线内容并将结果保存在本地的csv文件中

import requests,os
import csv
import time

page_number = 1
limit = 10
after_id = 0
rows = []

os.chdir('C:\\Users\\Viva Villa\\Desktop\\')
url =  'https://www.zhihu.com/api/v3/feed/topstory/recommend?'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}
cookies = {'Cookies': ***}
params = {'session_token': '945c610b517e955e2e59b9daf88e81b8','desktop':'true','page_number': page_number,'limit': limit,'action':'down','after_id':after_id}

for i in range(10):
  
    try:
        req = requests.get(url,headers = headers,cookies = cookies)
        time.sleep(2)
    except:
        print('未查找到网页')
        
    datas = req.json().get('data')
    for data in datas:
        target = data.get('target')
        target_id = target.get('id')
        target_type = target.get('type')
        headline = target.get('author').get('headline')
        name = target.get('author').get('name')
        voteup_count = target.get('voteup_count')
        thanks_count = target.get('thanks_count')
        comment_count = target.get('comment_count')
        rows.append([target_id,target_type,headline,name,voteup_count,thanks_count,comment_count])
    print ('第%d页数据下载完成'%page_number)
    page_number += 1
    after_id += 5

#每一项数据生成一个列表，作为一行，写入进 zhihu.csv 文件    
headers = ['id','type','headline','name','voteup_count','thanks_count','comment_count']
with open('zhihu.csv', 'w') as f:
    f_csv = csv.writer(f)
    f_csv.writerow(headers)
    for j in rows:
        f_csv.writerow(j)

print ('数据已经保存到zhihu.csv文件中')
