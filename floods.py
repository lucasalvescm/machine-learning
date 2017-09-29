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
key_1 = 'd3217c6d0e7a9cca'
key_2 = '556c01eefe7043a5'
key_3 = 'cb59574428ef5910'
key_4 = 'c632aab353bc8170'

# def update_climate_api():
#     cursor.execute("select * from data_climate where json_data is Null;")
#     data_ = list(cursor.fetchall())
#     count = 1
#     for dt in data_:
#         if count<=530:
#             #import ipdb;ipdb.set_trace()
#             id_dt = dt[0]
#             latitude = dt[4]
#             longitude = dt[5]
#             data = dt[1].replace('-','')
#             print('REQUISICOES: '+str(count))
#             try:
#                 url = 'http://api.wunderground.com/api/{}/history_{}/q/{},{}.json'.format(key_4,data,latitude,longitude)
#                 print(url)
#                 r = requests.get(url)
#                 json_content = json.loads(r.text)
                
#                 query = 'UPDATE data_climate SET json_data="{}" WHERE id="{}"'.format(str(json_content),id_dt)
#                 #print(query)
#                 cursor.execute(query)
#                 cursor.fetchall()
#                 db.commit()
#             except Exception as e:
#                 print(str(e)) 
#             count+=1    
#             time.sleep(15)   
#         else:
#             break

def analisando_dados():
    cursor.execute("select * from data_climate where json_data is not Null")
    data_ = list(cursor.fetchall())
    count = 0
    for dt in data_:
        
        
        json_data = dt[3]
        json_data = json_data.replace("'",'"')

        json_content = json.loads(json_data)
        
        try:
            
            if json_content['history']['dailysummary'] == []:
                print('erro')
                count+=1
            else:
                #print(json_content['history']['dailysummary'])
                pass
        except:
            pass

    print(count)

analisando_dados()
# update_climate_api()
 
def read_csv():
    data = pd.read_csv('datas_json_preenchido.csv')
    
    for id_date,data,id_event,json_data,flood,latitude,longitude in zip(data['id'],data['data_event'], data['id_event'], data['json_data'],data['flood'],data['latitude'],data['longitude']):
        print(id_date,data,id_event,str(json_data),flood,latitude,longitude)
        
        json_data = str(json_data)
        if json_data == 'nan':
            json_data = 'NULL'
        else:
            pass
        #import ipdb;ipdb.set_trace()
        
        query = 'UPDATE data_climate set json_data = "{}" where data_event="{}" and id_event={};'.format(json_data,data,id_event)
        print(query)
        cursor.execute(query)
        cursor.fetchall()
        db.commit()
         





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

        previous_date = began - timedelta(days=60)
        next_date = ended + timedelta(days=60)

        #list_dates = pd.date_range(previous_date, began).tolist() #Usado para inserir datas anteriores ao evento
        list_dates = pd.date_range(ended, next_date).tolist() #Usado para inserir datas após ao evento
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
