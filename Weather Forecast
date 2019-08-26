import requests
count = 0

while count < 5:
     
    while count < 5:
        city = input('请输入城市名字：')
        
        # 只允许输入汉字
        if city >= u'\u4e00' and city <=u'\u9fa5':
            print(end='')
            count += 1
        else:
            print ('请输入汉字：')
            count += 1
            continue
            
        try:
            req = requests.get('http://wthrcdn.etouch.cn/weather_mini?city=%s'% city)
        except Exception as e:
            print('查询失败:%s'%e)
            break

        dic_city = req.json()
        city_data = dic_city.get('data')

        while city_data:
            forecast = city_data['forecast'][:]
            print(city+'未来五日的天气预报如下：')
            for a in forecast:
                print(a['date'],a['high'],a['low'],a['type'],sep=',')
            break

    else:
        print('''输入错误超过5次，程序自动退出
重新开始请输入Restart''')

    if input() == 'Restart':
        print ('请再次输入城市名称：')
        count = 0
    else:
        break
