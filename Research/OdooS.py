import xmlrpc.client
import pyodbc

#info = xmlrpc.client.ServerProxy('https://demo.odoo.com/start').start()
#url, db, username, password = info['host'], info['database'], info['user'], info['password']


#url="https://demo5.odoo.com"
#db="demo_130_1601974830"
#username="admin"
#password="admin"
#tuico:tsxs9cp3yP3MJHYq@t
#url="https:///uico-staging.trobz.com"
#url="tuico:tsxs9cp3yP3MJHYq@https://erp.tuicovn.com"
#db="tuico_live"

url="https://tuico.odoo.com"
username="toan@tuicovn.com"
password="toan@4967"
db="tuico"


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

#tupleItem = ("AF80--113","N70--008IR")
#print(tupleItem)

#[[['name', 'in',("AF80--113","N70--008IR")]]],
#print(tupItem)
thisdict={}
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
	thisdict["weight"] = wtpc_dict[row["name"]]
	thisdict["list_price"] =id*1.5
	print(thisdict)
	models.execute_kw(db, uid, password, 'product.template', 'write', [[id],thisdict])
	#print(id)
quit()

"""
r=models.execute_kw(db, uid, password,
    'product.product', 'search_read',
    [[['name', '=', 'N70--001']]],
    {'fields': ['name'], 'limit': 5})
    
models.execute_kw(db, uid, password,
    'res.partner', 'search_read',
    [[['is_company', '=', True], ['customer', '=', True]]],
    {'fields': ['name', 'country_id', 'comment'], 'limit': 5})

models.execute_kw(db, uid, password,
	'res.partner', 'search_read',
	[[['is_company', '=', True]]],
	{'fields': ['name', 'country_id', 'comment'], 'limit': 5})
quit()
"""


"""
	id = models.execute_kw(db, uid, password, 'res.partner', 'create', [{
    		'name': "New Partner",
			}])
	print(id)


	models.execute_kw(db, uid, password, 'res.partner', 'write', [[58], {
	    'name': "Newer partnerAAA"
	}])	

	a=models.execute_kw(db, uid, password, 'res.partner', 'name_get', [[10]])
	print(a)

	record=models.execute_kw(db, uid, password,
    	'res.partner', 'search_read',
    	[[['is_company', '=', True]]],
    	{'fields': ['name', 'country_id', 'comment'], 'limit': 5})
    
	for row in record:
		print(row["name"])
"""
