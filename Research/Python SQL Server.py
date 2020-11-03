import pyodbc 
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=192.168.0.1;'
                      'Database=O-Ring Material;'
                      'uid=sa;pwd=356112342597')
cursor = conn.cursor()
cursor.execute("select TuicoNo,Wtpcs From tblProducts where TuicoNo in ('AF80--113','N70--007A')")
for row in cursor:
    print(row[1])

    