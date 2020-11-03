import logging
import xmlrpc.client

#url="https://tuico:tsxs9cp3yP3MJHYq@erp.tuicovn.com"
url="https://tuico:tsxs9cp3yP3MJHYq@tuico-staging.trobz.com"
username="toan@tuicovn.com"
password="toan@4967"
db="tuico_stag"

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})

if uid ==0:		
	print("Loi Dang Nhap")
	#logging.error('Dang nhap sai')
	quit()	
#print("Dang Nhap OK")	


models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
order_id=models.execute_kw(db, uid, password,
	    'sale.order', 'search',
	    [[['name', '=','9320019']]])

if len(order_id)==0:
	print("Ko Tim Thay")	
	quit()


#models.execute_kw(db, uid, password, 'sale.order', 'action_confirm', order_id)
#models.execute_kw(db, uid, password, 'sale.order', 'action_delete_lines', order_id)
#models.execute_kw(db, uid, password, 'sale.order', 'action_draft', order_id)
quit()

#print(ids[0])	
try :

	print("Confirm Ok")
except:
	errDes="Error: order_confirm"
	print(errDes);
	#logging.error(errDes)