# 在智联招聘中，抓取 python 相关职位信息和详细职位描述，保存数据到本地csv文件
import requests,csv,time
from bs4 import BeautifulSoup

def get_info():
    req = requests.get(url,headers = headers,cookies = cookies).json()   
    if req.get('code')==200:          
        all_jobs = req.get('data').get('results')
        rows = []
        for i in all_jobs:             #获取本页面信息
            job_name = i.get('jobName')
            company_name = i.get('company').get('name')
            company_type = i.get('company').get('type').get('name')
            company_size = i.get('company').get('size').get('name')
            company_url = i.get('company').get('url')
            job_city = i.get('city').get('display')
            job_salary = i.get('salary')
            job_level = i.get('eduLevel').get('name')
            job_type_list = i.get('jobType').get('items')  #列表[{"name":"软件/互联网开发/系统集成"}]
            job_type = [item[key] for item in job_type_list for key in item]   #列表['软件/互联网开发/系统集成']
            try:
                job_workingExp = i.get('workingExp').get('name')      #'workingExp'字典{'name': '3-5年'} 有部分空白
            except:
                job_workingExp = None
            job_emplType = i.get('emplType')
            welfare_list = i.get('welfare')   #列表
            welfare = ','.join(welfare_list)
            job_details = [job_name,company_name,company_type,company_size,company_url,job_city,job_salary,job_level,*job_type,job_workingExp,job_emplType,welfare]
            rows.append(job_details)
        return rows    #得到一页的数据
        
datas = []
for page_number in range(0,270,90):    #一次爬取三页，一页有90个招聘信息
    url = 'https://fe-api.zhaopin.com/c/i/sou?start=%d&pageSize=90&cityId=801&salary=0,0&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kw=Python&kt=3&=0&_v=0.95294310&x-zp-page-request-id=93ff1df90079470b81ec654224ae1391-1567932557926-449024&x-zp-client-id=37993489-8ff4-453a-f754-df8a21cccd4a'%page_number
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}
    cookies = {'Cookies': 'Cookie: acw_tc=2760828b15677647804857503e9e7c2b32fa2ee12dd352be4bb7d7b7bb1633'}
    rows = get_info()
    print ('正在下载第%d页的招聘信息'%int(page_number//90+1))
    datas.append(rows)
    time = 2
    
headers = ['工作名称','公司名称','公司类型','公司规模','公司链接','所在城市','薪水','学历要求','工作类型','期限','雇佣类型','福利']
with open('zhaopin.csv', 'w', newline='') as f:
    f_csv = csv.writer(f)
    f_csv.writerow(headers)
    for data in datas:
        for j in data:
            f_csv.writerow(j)
print ('数据已保存至lianjia.csv')
