import xmlrpc.client
import pyodbc

#-------- Get Date From SQL Server ---------
tupItem =()
#tupWtpcs =()
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

#---------- Update Odoo -----------------
url="https://tuico:tsxs9cp3yP3MJHYq@erp.tuicovn.com"
username="synchdata@tuicovn.com"
password="dtSynxgad2!~od321"
db="tuico_live"

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})

if uid ==0:
	print('Dang nhap sai')
	quit()	

print('OK Good')
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

#tupleItem = ("AF80--113","N70--008IR")
#print(tupleItem)

#[[['name', 'in',("AF80--113","N70--008IR")]]],
#print(tupItem)
product_dict={}
record=models.execute_kw(db, uid, password,
	    'product.template', 'search_read',
	    [[['name', 'in',tupItem]]],
	    {'fields': ['name'], 'limit': 5})
print(record)
for row in record:	
	id=row["id"]	
	#print(row["name"])
	#print(wtpc_dict[row["name"]])
	#lay wieght luu trong Dic

	#product_dict["weight"] = wtpc_dict[row["name"]]
	product_dict["purchase_ok"] = 0
	
	#thisdict["list_price"] =id*1.5
	print(product_dict)
	models.execute_kw(db, uid, password, 'product.template', 'write', [[id],product_dict])
	#print(id)
quit()

