import requests,time,sqlite3,datetime,pandas
from bs4 import BeautifulSoup

def datetime1():
    print('日期格式:(20200101)')
    st = input('請輸入起始日期:')
    et = input('請輸入最終日期:')
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
    print('天數:',len(date))
    main_data = []
    date1 = []
    date_count = 0
    for x in date:
        print(main_data)
        print(date_count)
        url = "https://www.cnyes.com/futures/History.aspx?mydate={}&code=CDCS".format(x)
        r = requests.get(url)
        print('連接狀態:',r.status_code)
        sp = BeautifulSoup(r.text,'lxml')
        tabs1 = sp.find_all('div',{'class':'tabs1'})
        field = tabs1[0].find('table').find_all('th')
        data = tabs1[0].find('table').find_all('tr')[1].find_all('td')
        cr = [] #data
        if len(data) == 5:
            print('已找到資料!')
            for i in data:
                cr.append(i.string)
                date1.append(x)
            main_data.append(cr)
        else:
            print('資料不符合!')
        fields = [] #row
        for i in field:
            fields.append(i.string)
        time.sleep(0.5)
        date_count+=1
    return fields,main_data,date1


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
print(dict)
print(len(dict['開盤']),len(dict['最高']),len(dict['最低']),len(dict['收盤']),len(dict['成交量']),len(dict['日期']))
#df = pandas.DataFrame(dict)
#df.set_index('日期',inplace=True)
#print(df)
#df.to_csv('test.csv')