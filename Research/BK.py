tuplex = (4, 6, 2, 8, 3, 1) 
print(tuplex)
#tuples are immutable, so you can not add new elements
#using merge of tuples with the + operator you can add an element and it will create a new tuple
tuplex =("9","s1")
print(tuplex)
quit()	


info = xmlrpc.client.ServerProxy('https://demo.odoo.com/start').start()
url, db, username, password = info['host'], info['database'], info['user'], info['password']
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))


uid = common.authenticate(db, username, password, {})
if uid ==0:
	print('Dang nhap sai')
	quit()

models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
ok=models.execute_kw(db, uid, password,
    'res.partner', 'check_access_rights',
    ['read'], {'raise_exception': False})
if ok:
	ids = models.execute_kw(db, uid, password,
	    'res.partner', 'search',
	    [[['is_company', '=', True]]],
	    {'limit': 1})
	[record] = models.execute_kw(db, uid, password,
	    'res.partner', 'read', [ids])
	# count the number of fields fetched by default
	print([record])



