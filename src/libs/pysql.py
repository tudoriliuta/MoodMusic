import pyodbc
server = 'tcp:emusicserver.database.windows.net'
database = 'emusicdb'
username = 'trevor'
password = 'park345$$'
driver= '{ODBC Driver 13 for SQL Server}'
cnxn = pyodbc.connect('DRIVER='+driver+';PORT=1433;SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

cursor.execute("SELECT * FROM dbo.sysdatabases")
row = cursor.fetchone()
while row:
    print str(row[0]) + " " + str(row[1])
    row = cursor.fetchone()



with cursor.execute("INSERT INTO Track ( Trackid, TrackName, TrackLabel) OUTPUT INSERTED.Trackidkey VALUES ('3n3Ppam7vgaVa1iaRUc9L', 'Track Name ', 'Track Label')"): 
    print ('Successfuly Inserted!')
cnxn.commit()
