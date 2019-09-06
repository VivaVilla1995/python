import requests
import csv
import re
from bs4 import BeautifulSoup

# 获取数据
def lianjia_get():
    req = requests.get(url,headers = headers,cookies = cookies)
    req_html = req.text
    soup = BeautifulSoup(req_html,'html.parser')    # html解析器
    all_data = soup.find_all('div',class_='content__list--item--main')
    all_info = []
    # 依次寻找每个房源的详细页链接、位置、面积、朝向和户型等信息
    for i in all_data:
        link = 'https://sh.lianjia.com'+ i.find('p',class_='content__list--item--title twoline').find('a').get('href')
        des = i.text
        des1 = re.split('\n',des)    # 转换成列表
        des2 = [i.strip() for i in des1 if (len(i.strip())!=0)]   # 去掉列表空元素
        
        # ['整租·杜鹃园 1室1厅 南', '徐汇-康健-杜鹃园', '/', '43㎡', '/南        /', '1室1厅1卫', '/', 
        # '低楼层                        （6层）', '贝壳优选', '1天前发布', '近地铁', '精装', '新上', '随时看房', '4700 元/月']
        
        title = des2[0]
        #address = des2[1]
        area = des2[3]
        #direction = des2[4].strip('/').replace(' ','')
        #style = des2[5]
        high = des2[7].replace(' ','')
        time = des2[9]
        advantage = des2[-2]+' '+des2[-3]+' '+des2[-4]+' '+des2[-5]
        price = des2[-1]
        details = [title, area, high, time, advantage, price, link]
        
        # ['整租·杜鹃园 1室1厅 南', '徐汇-康健-杜鹃园', '43㎡', '南', '1室1厅1卫', '低楼层（6层）', '1天前发布', 
        # '随时看房 新上 精装 近地铁', '4700 元/月', 'https://sh.lianjia.com/zufang/SH2338491530580598784.html']
        
        all_info.append(details)
    return all_info
    
# 下载数据
rows = []
page_number = 1
for i in range(5):     # 一个csv文件写入5页的数据
    url = 'https://sh.lianjia.com/zufang/pg%d/#contentList'%page_number
    cookies = {'Cookies': 'lianjia_ssid=f354efd8-f1ff-4a52-a4c9-17145f9b5710; lianjia_uuid=c2981347-edac-4b80-a2be-1a11308724be; all-lj=ed5a77c9e9ec3809d0c1321ec78803ae; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiNmFiOTNmYjNhYTJjY2UzNThmNmFkNjljNGJmMzJhYWViMjYyMDA1ZDY3ZjE4N2EzZjAzYmMzYjI0YjA1MTZmYmI2MTExYjBjZjYyN2RlN2NjYzY2OGU3YWE2MTBjYmVmMWJjM2ZkZTM2MGQ4ZjY3YzE0YmNiMzNmOWYxYTA3OWViY2ZhMzZjMjU2Y2E2N2ViNTIyN2YwYzg2MDAxZjFmZGFhMDcwYzBkMzU3MjQ5OGM1MzllOWE0MzMxN2RkNmFkZDU2ZDE5OTZkOGY0MzgyNDAyMTEyZjQyZTQyNzc3ZmZlMTIwZWU4NjFlYTczN2JhMzQ3OTBjMjg3ZGM3NGJkMmFiNDgwYThhYmU0NDkyNGU3YzEzNzdkNGIwYmExZjA5ZjA4NDY0NTY5NTYwM2QzMGEwOTg4NDgzZGJlMmUxN2M0YjhkOTM2NzBiM2MxNjIwZjgwMGVlMzVhNzBkMmZjYlwiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCI4NjBmNTJmYlwifSIsInIiOiJodHRwczovL3NoLmxpYW5qaWEuY29tL3p1ZmFuZy8iLCJvcyI6IndlYiIsInYiOiIwLjEifQ=='}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}
    data = lianjia_get()
    print ('正在下载数据')
    rows.append(data)
    page_number += 1

headers = ['title', 'area', 'high', 'time', 'advantage', 'price', 'link']
with open('lianjia.csv', 'w', newline='') as f:
    f_csv = csv.writer(f)
    f_csv.writerow(headers)
    for row in rows:
        for i in row:
            f_csv.writerow(i)
print ('数据已保存至lianjia.csv')
