import MySQLdb
from datetime import datetime
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
#import ipdb;ipdb.set_trace()
cursor.execute("SELECT * FROM floods;")
data = list(cursor.fetchall())
# d2 = dict((k, v) for k, v in dict_months.items())
# for d in data:

#     data = str(d[10]).split('-') if d != '#N/DISP' else ''



#     try:
#         #import ipdb;ipdb.set_trace()
#         day = data[0]
#         month = d2[str(data[1])]
#         year = '19'+str(data[2]) if (int(data[2]) > 84 and int(data[2]) <= 99) else '20'+str(data[2])
#         date = str(year)+'-'+str(month)+'-'+str(day)
        
#         date = datetime.strptime(date, '%Y-%m-%d')

#         #import ipdb;ipdb.set_trace()

#         cursor.execute("UPDATE floods SET Ended='{}' WHERE Register='{}'".format(str(date),int(d[0])))

#         cursor.fetchall()

#         db.commit()


#     except Exception as e:

#         print (str(e))
#         pass
dict_country = {}
for d in data:
    if d[3] == 'Brazil':
        import ipdb;ipdb.set_trace()
    try:
        c = dict_country[str(d[3])]
        c = c+1

        c.UPDATE({str(d[3]):c})
    except:
        #import ipdb;ipdb.set_trace()
        dict_country.update({str(d[3]):1})



print (dict_country)


