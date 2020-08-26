import requests,time,sqlite3,datetime,pandas
from bs4 import BeautifulSoup

def datetime1():
    st = '20200101'
    et = '20200103'
    StartDate = time.strptime(str(st), "%Y%m%d")
    EndDate = time.strptime(str(et), "%Y%m%d")
    StartDate = datetime.date(StartDate[0], StartDate[1], StartDate[2])
    EndDate =  datetime.date(EndDate[0], EndDate[1], EndDate[2])
    RangeDate = datetime.timedelta(days = 1)
    date = []
    while StartDate <= EndDate:
        StartDate = StartDate + RangeDate
        date.append(str(StartDate).replace('-',''))
    return date

def download():
    date = datetime1()
    main_data = []
    date_count = 0
    for x in date:
        url = "https://www.cnyes.com/futures/History.aspx?mydate={}&code=CDCS".format(x)
        r = requests.get(url)
        print(r.status_code)
        sp = BeautifulSoup(r.text,'lxml')
        tabs1 = sp.find_all('div',{'class':'tabs1'})
        field = tabs1[0].find('table').find_all('th')
        data = tabs1[0].find('table').find_all('tr')[1].find_all('td')
        print(len(data))
        cr = [] #data
        if len(data) == 5:
            for i in data:
                cr.append(i.string)
        else:
            date.pop(date_count)
        main_data.append(cr)
        fields = [] #row
        for i in field:
            fields.append(i.string)
        time.sleep(0.5)
        date_count+=1
    return fields,main_data,date

data = download()[0:]
f = data[0]
d = data[1]
date = data[2]
#開盤 最高 最低 收盤 成交量
d1,d2,d3,d4,d5 = [],[],[],[],[]
for i in range(len(d)):
    for x in range(len(d[i])):
        if x == 0:
            d1.append(d[i][x])
        elif x == 1:
            d2.append(d[i][x])
        elif x == 2:
            d3.append(d[i][x])
        elif x == 3:
            d4.append(d[i][x])
        elif x == 4:
            d5.append(d[i][x])
dict = {f[0]:d1,f[1]:d2,f[2]:d3,f[3]:d4,f[4]:d5,'日期':date}
df = pandas.DataFrame(dict)
df.set_index('日期',inplace=True)
print(df)
df.to_csv('test.csv')