import xmlrpc.client
import pyodbc

url="https://tuico.odoo.com"
username="toan@tuicovn.com"
password="toan@4967"
db="tuico"

tupItem =()
wtpc_dict={}
connSQL = pyodbc.connect('Driver={SQL Server};'
                      'Server=192.168.0.1;'
                      'Database=O-Ring Material;'
                      'uid=sa;pwd=356112342597')
SqlRs = connSQL.cursor()
SqlRs.execute("select TuicoNo,Round(Wtpcs,5) as Wtpcs From tblProducts where TuicoNo in ('AF80--113','N70--007A','N70--008IR')")
for rowSQL in SqlRs:
	tupItem=tupItem+(rowSQL[0],)
	#tupWtpcs=tupWtpcs+(rowSQL[1],)
	wtpc_dict[rowSQL[0]] = rowSQL[1]
    #print(rowSQL[0])

#print(tupItem)
#print(wtpc_dict["N70--007A"])
#quit()

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})

if uid ==0:
	print('Dang nhap sai')
	quit()	

models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
rs=models.execute_kw(db, uid, password,
	    'product.template', 'search_read',
	    [[['name', 'in',tupItem]]],
	    {'fields': ['name','standard_price'], 'limit':5})
print(rs)
for row in rs:	
	id=row["id"]
	print(row["name"])
	print(row["standard_price"])	
	#print(wtpc_dict[row["name"]])

	
	thisdict={}
	#---lay wieght luu trong Dic---
	thisdict["weight"] = wtpc_dict[row["name"]]
	thisdict["list_price"] =id*1.5
	#print(thisdict)
	models.execute_kw(db, uid, password, 'product.template', 'write', [[id],thisdict])
	#print(id)

quit()


