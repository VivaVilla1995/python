import requests,os
import csv
import pandas as pd

lat = str(input('latitude(eg.-30.00):'))
lon = str(input('longitude(eg.135.00):'))
start = int(input('start(eg.20160101):'))
finish = int(input('finish(eg.20160105):'))
username = str(input('username(eg.1059571137846140675):'))
variables = str(input('''variables:
R for daily_rain;
X,N for max_temp and min_temp;
V,D for vp and vp_deficit;
E,S,C for evap_pan,evap_syn,evap_comb,evap_morton_lake;
J for radiation;
H,G for rh_tmax and rh_tmin;
F,T,A,P,W for et_short_crop,et_tall_crop,et_morton_actual,et_morton_potential,et_morton_wet;
M for mslp;
'''))

# 如果想输出所有变量，则去掉variables和comment=部分
api_url = 'https://www.longpaddock.qld.gov.au/cgi-bin/silo'
params = 'format=json&lat=%s&lon=%s&start=%s&finish=%s&comment=%s&username=%s&password=silo'%(lat,lon,start,finish,variables,username)
url =  api_url + '/DataDrillDataset.php?' + params

# 得到针对data science的文件格式
req = requests.get(url).json()
items = req.get('data')

#[{'date': '2016-01-01', 'variables': 
#  [{'source': 25, 'value': 0.0, 'variable_code': 'daily_rain'}, 
#   {'source': 25, 'value': 36.0, 'variable_code': 'max_temp'}, 
#   {'source': 25, 'value': 20.0, 'variable_code': 'min_temp'}]}, 
# {'date': '2016-01-02', 'variables': 
#  [{'source': 25, 'value': 0.0, 'variable_code': 'daily_rain'}, 
#   {'source': 25, 'value': 37.0, 'variable_code': 'max_temp'}, 
#   {'source': 25, 'value': 20.5, 'variable_code': 'min_temp'}]}]

#param = []
for i in range(len(items)):
    date = items[i].get('date')
    variables = items[i].get('variables')
    var1 = []
    var2 = []
    for j in range(len(variables)):
        code = variables[j].get('variable_code')
        value = variables[j].get('value')
        var1.append(code)
        var2.append(value)
    #param.append([date,*var1,*var2])
        
        header = ['date','name','value']
        with open(r'C:\Users\Viva Villa\Desktop\data_%s.csv'%code, 'w') as f:
            f_csv = csv.writer(f)
            f_csv.writerow(header)
            f_csv.writerows(zip(date,var1,var2))
        csv_data = pd.read_csv(r'C:\Users\Viva Villa\Desktop\data_%s.csv'%code)
        csv_df = pd.DataFrame(csv_data)
        csv_df.to_csv(r'C:\Users\Viva Villa\Desktop\data_%s.csv'%code)         

# param [['2016-01-01', 'daily_rain', 'max_temp', 'min_temp', 0.0, 36.0, 20.0], 
#        ['2016-01-02', 'daily_rain', 'max_temp', 'min_temp', 0.0, 37.0, 20.5]]
