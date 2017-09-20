import MySQLdb
from datetime import datetime,timedelta
import requests
import json
from statistics import mean
import time
import pandas as pd
# Open database connection
db = MySQLdb.connect("localhost","root","root","flood_db" )
# prepare a cursor object using cursor() method
cursor = db.cursor()
# execute SQL query using execute() method.
dict_months={
    'Jan':1,
    'Feb':2,
    'Mar':3,
    'Apr':4,
    'May':5,
    'Jun':6,
    'Jul':7,
    'Aug':8,
    'Sep':9,
    'Oct':10,
    'Nov':11,
    'Dec':12,
}


def update_climate_api():
    cursor.execute("select * from data_climate where json_data is Null;")
    data_ = list(cursor.fetchall())
    
    for dt in data_:
        id_dt = dt[0]
        latitude = dt[4]
        longitude = dt[5]
        data = dt[1].replace('-','')
        print(id_dt)
        try:
            url = 'http://api.wunderground.com/api/556c01eefe7043a5/history_{}/q/{},{}.json'.format(data,latitude,longitude)
            #print(url)
            r = requests.get(url)
            json_content = json.loads(r.text)
            
            query = 'UPDATE data_climate SET json_data="{}" WHERE id="{}"'.format(str(json_content),id_dt)
            print(query)
            cursor.execute(query)
            cursor.fetchall()
            db.commit()
        except Exception as e:
            print(str(e)) 

        time.sleep(30)   


 
update_climate_api()


def insert_dates():
    '''
    Select na tabela de floods pegando as datas de cada evento e atualizando na tabela de data_climate.
    '''
    cursor.execute("select * from floods where Centroid_X != '#N/DISP' and Centroid_Y != '#N/DISP' and Country like 'USA';")
    data_ = list(cursor.fetchall())
    d2 = dict((k, v) for k, v in dict_months.items())



    for dt in data_:
        #if dt[31] is None:
        latitude = dt[20].replace(',','.')
        longitude = dt[19].replace(',','.')
        began = dt[9]
        ended = dt[10]
        #print("Latitude:"+latitude+" Longitude:"+longitude+" Inicio:"+began+" Fim:"+ended)
        #import ipdb;ipdb.set_trace()

        began = datetime.strptime(began, "%Y-%m-%d %H:%M:%S")
        ended = datetime.strptime(ended, "%Y-%m-%d %H:%M:%S")

        previous_date = began - timedelta(days=20)

        list_dates = pd.date_range(previous_date, began).tolist() #Usado para inserir datas anteriores ao evento
        #list_dates = pd.date_range(began, ended).tolist() #Usado para inserir datas durante o evento.
        for date in list_dates:
            try:
                #import ipdb;ipdb.set_trace()
                date_string = str(date.strftime('%Y-%m-%d'))
                query = "INSERT INTO data_climate (data_event, id_event,flood,latitude,longitude) VALUES ('{}',{},0,{},{});".format(date_string,dt[0],latitude,longitude)
                print(query)
                cursor.execute(query)
                cursor.fetchall()

                db.commit()
            except Exception as e:
                print(str(e))
            #import ipdb;ipdb.set_trace()


        # date_format = began[:10].replace('-','')
        # latitude_format = latitude.replace(',','.')
        # longitude_format = longitude.replace(',','.')
        # try:
        #     url = 'http://api.wunderground.com/api/556c01eefe7043a5/history_{}/q/{},{}.json'.format(date_format,latitude_format,longitude_format)
        #     #print(url)
        #     r = requests.get(url)
        #     json_content = json.loads(r.text)

        #     list_hum = []
        #     list_temp = []
        #     list_prec = []
        #     list_pressure = []

        #     for j in json_content['history']['observations']:
        #         if '1'in j['rain']:
        #             print (j['hum'])
        #             print (j['tempm'])
        #             print (j['precipi'])
        #             print (j['rain'])
        #             print ('----------')

        #             list_prec.append(float(j['precipm'])) if j['precipm'] != "" else ''
        #             list_temp.append(float(j['tempm'])) if j['tempm'] != "" else ''
        #             list_hum.append(float(j['hum'])) if j['hum'] != "" else ''
        #             list_pressure.append(float(j['pressurei'])) if j['pressurei'] != "" else ''

            
        #     media_hum = mean(list_hum)     
        #     media_temp = mean(list_temp)
        #     media_prec = mean(list_prec)
        #     media_ppressure = mean(list_pressure)         

            
        #     #     print(json_content['history']['observations'])
        #     # else:
        #     #     pass
        #     cursor.execute("UPDATE floods SET temperature='{}', humidity='{}', precipitation='{}', pressure='{}' WHERE Register='{}'".format(media_temp,media_hum,media_prec,media_ppressure,str(dt[0])))
        #     cursor.fetchall()

        #     db.commit()

        #     time.sleep(30)
        # except Exception as e:
        #     if 'string' in str(e):
        #         import ipdb;ipdb.set_trace()
        #     pass

        # time.sleep(20)

def update_dates(data):
    pass
    # for d in data:
    # data = str(d[9]).split('-') if d != '#N/DISP' else ''
    # try:
    #     #import ipdb;ipdb.set_trace()
    #     day = data[0]
    #     month = d2[str(data[1])]
    #     year = '19'+str(data[2]) if (int(data[2]) > 84 and int(data[2]) <= 99) else '20'+str(data[2])
    #     date = str(year)+'-'+str(month)+'-'+str(day)
        
    #     date = datetime.strptime(date, '%Y-%m-%d')

    #     #import ipdb;ipdb.set_trace()

    #     cursor.execute("UPDATE floods SET Began='{}' WHERE Register='{}'".format(str(date),int(d[0])))

    #     cursor.fetchall()

    #     db.commit()
    # except Exception as e:

    #     print (str(e))
    #     pass

