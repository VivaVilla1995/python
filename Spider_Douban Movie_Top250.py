import requests,os
import csv
import time
# import pandas as pd

# Part1: 获得电影 “肖申克的救赎”的电影海报 url 地址，下载电影海报到本地
 
def get_poster():                  # 获取海报下载地址
    req_poster = requests.get('https://api.douban.com/v2/movie/1292052?apikey=0df993c66c0c636e29ecbb5344252a4a')
    poster_data = req_poster.json()
    image_url = poster_data.get('image')
    return image_url

def save_image():                  # 下载海报
    req_image = requests.get(get_poster())
    image = req_image.content
    with open(r'C:\Users\Viva Villa\Desktop\image.jpg','wb') as f:
        f.write(image)

# Part2: 批量获取250部电影的电影名、主演、评分等数据，保存数据到本地 csv 文件

def data_csv(): 
    data = []
    for start in range(0,250,20):           # 设置翻页 
        req_data = requests.get('https://api.douban.com/v2/movie/top250?start= %d &apikey=0df993c66c0c636e29ecbb5344252a4a'%start)
        movie_data = req_data.json()
        movie_subjects = movie_data.get('subjects')
        
        images_url = []
        for i in range(len(movie_subjects)):
                each_title = movie_subjects[i].get('title')
                rating_value = movie_subjects[i].get('rating')
                each_score = rating_value.get('average')
                each_genres = movie_subjects[i].get('genres')
                each_durations = movie_subjects[i].get('durations')
                each_url = movie_subjects[i].get('images').get('small')

                casts_value = movie_subjects[i].get('casts')       # 获取casts需要再get一次，再get每个name
                casts_list=[]
                for j in range(len(casts_value)): 
                    each_cast = casts_value[j].get('name')
                    casts_list.append(each_cast)                  # 输出name存在列表

                data.append([each_title,each_score,', '.join(each_genres),', '.join(each_durations),','.join(casts_list),each_url])
    return data
                
def save_csv():
    #movie = pd.DataFrame(columns = headers,data = data_csv())
    #movie.to_csv(r'C:\Users\Viva Villa\Desktop\movie.csv')         #如果生成excel，可以用to_excel
    
    headers = ['电影名称','电影评分','电影类型','电影时长','演员列表','海报链接']
    with open(r'C:\Users\Viva Villa\Desktop\movie.csv', 'w') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        f_csv.writerows(data_csv())
        
# Part3: 获取每一部电影海报的url，批量下载电影海报到本地

def save_all_images():
    
    all_url = ['https://api.douban.com/v2/movie/top250?start={}&apikey=0df993c66c0c636e29ecbb5344252a4a'.format(k) for k in range(0,250,20)]
    for url in all_url:
        req_images = requests.get(url).json()
        movie_subjects = req_images.get('subjects')
        for j in range(len(movie_subjects)):
            each_url = movie_subjects[j].get('images').get('small')
            each_title = movie_subjects[j].get('title')
            images = requests.get(each_url).content
            with open(r"C:\Users\Viva Villa\Desktop\movies\{}.jpg".format(each_title),"wb") as f:
                f.write(images)
        time.sleep(2)
        
if __name__ == '__main__':
    save_image()
    save_csv()
    save_all_images()
