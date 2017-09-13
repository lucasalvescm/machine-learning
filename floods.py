import MySQLdb
# Open database connection
db = MySQLdb.connect("localhost","root","root","flood_db" )
# prepare a cursor object using cursor() method
cursor = db.cursor()
# execute SQL query using execute() method.
cursor.execute("SELECT * FROM floods;")
data = list(cursor.fetchall())
for d in data:
    print("Latitude",d[19])
    print("Longitude",d[20])