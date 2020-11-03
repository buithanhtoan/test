import pyodbc 
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=192.168.0.1;'
                      'Database=O-Ring Material;'
                      'uid=sa;pwd=356112342597')

cursor = conn.cursor()
SQL= "select TuicoNo,Wtpcs From tblProducts where TuicoNo in ('AF80--113','N70--007A')"
cursor.execute(SQL)
#print(cursor)
while True:
	row = cursor.fetchone()
	if not row:
		break
	print(row)
#conn.close()
cursor.close()

"""
conn2 = pyodbc.connect('Driver={SQL Server};'
                      'Server=192.168.0.1;'
                      'Database=O-Ring Material;'
                      'uid=sa;pwd=356112342597')

cursor2 = conn.cursor()
cursor2.execute("select TuicoNo,Wtpcs From tblProducts where TuicoNo in ('AF80--113','N70--007A')")
print(cursor2)
for row in cursor2:
    print(row)


"""
