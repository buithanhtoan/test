#----- Chuong Trinh Import Old Order Data  vo odoo -----
import logging
import xmlrpc.client
import pyodbc
from time import time
from datetime import datetime

url="https://tuico:tsxs9cp3yP3MJHYq@tuico-staging.trobz.com"
username="toan@tuicovn.com"
password="toan@4967"
db="tuico_stag"

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})

if uid ==0:		
	logging.error('Dang nhap sai')
	quit()	

models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

#------------*****  SQL Server  *****----------
connSQL = pyodbc.connect('Driver={SQL Server};'
                      'Server=192.168.0.1;'
                      'Database=O-Ring Material;'
                      'uid=sa;pwd=356112342597')
curs = connSQL.cursor()

curs.execute("Select Distinct OrderID,CustomerID,OrderDate,PONO,OrderDateCust,ActualReply,RequiredReply \
				From odoo_vwAllOrderDetails_Import \
				Where OrderID in('1220001')")
				#Order By OrderID,WorkingNo
rs = curs.fetchall()
for r in rs:

	ids=models.execute_kw(db, uid, password,'sale.order', 'search',[[['name', 'ilike',r.OrderID]]])
	if len(ids)==0:
		order={}
		print(r.OrderID)
		if r.CustomerID!='':
			ids=models.execute_kw(db, uid, password,'res.partner', 'search',[[['no', 'ilike',r.CustomerID]]])
			if len(ids)==0:
					errDes="Not found Customer: "+ r.CustomerID
					print(errDes)				
					#logging.error(errDes)
					continue
			else:				
				order["partner_id"]=ids[0]
				#print(ids[0])
		else:
			errDes="Not found Customer: "+ r.CustomerID
			print(errDes)
			#logging.error(errDes)
			continue

		order["po_no"]=r.PONO
		order["date_order"]=r.OrderDate.strftime("%Y-%m-%d %H:%M:%S")
		if not(r.OrderDateCust is None): order["customer_order_date"]=r.OrderDateCust.strftime("%Y-%m-%d %H:%M:%S")
		if not(r.ActualReply is None): order["actual_reply_date"]=r.ActualReply.strftime("%Y-%m-%d %H:%M:%S")
		if not(r.RequiredReply is None): order["required_reply_date"]=r.RequiredReply.strftime("%Y-%m-%d %H:%M:%S")
		#--- Insert Order ---
		order_id = models.execute_kw(db, uid, password, 'sale.order', 'create',[order])
		#------ Update Lai Order ID ------
		models.execute_kw(db, uid, password, 'sale.order', 'write',[[order_id],{'name':r.OrderID}])
	else:
		order_id=ids[0]
	#--End If Search Order
	continue
	#********************************   DETAILS   ************************************************
	#-----====== Detaill =====-------
	cursDt = connSQL.cursor()
	cursDt.execute("Select OrderID,WorkingNo,TuicoNo,Compound,Quantity,Price,ProduceQty,CustomerCpd,OrderType, \
							DeliveryDate_v, DeliveryConfirmation, OldConfirmDate, EstimatedshippingDate \
					From odoo_vwAllOrderDetails_Import \
					Where OrderID='" +r.OrderID +"' Order By OrderID,WorkingNo")  

	dt = cursDt.fetchall()
	count_error=0
	o_details=[]
	for d in dt:
		#print(d.OrderType)
		od={}		
		od["order_id"]=order_id
		od["line_no"]=d.WorkingNo

		#-------- Kiem Tra Product ------------
		ids=models.execute_kw(db, uid, password,'product.product', 'search',[[['default_code', 'ilike',d.TuicoNo]]])
		if len(ids)==0:
				errDes="Not found ProductNo: "+ d.TuicoNo + " Order:" + str(d.OrderID) + '-' + d.WorkingNo
				print(errDes)
				count_error=1
				#logging.error(errDes)
				continue
		else:				
			od["product_id"]=ids[0]
			
		#-------- Kiem Tra Compound ----------
		if d.Compound!='':
			ids=models.execute_kw(db, uid, password,'product.product', 'search',[[['default_code', 'ilike',d.Compound]]])
			if len(ids)==0:
					errDes="Not found Compound: "+ d.Compound + " Order:" +str(OrderID)+ '-' + d.WorkingNo
					print(errDes)
					count_error=1
					#logging.error(errDes)
					continue
			else:
				od["compound_id"]=ids[0]

		od["product_uom_qty"]=d.Quantity		
		od["price_unit"]=d.Price
		od["to_produce_qty"]=d.ProduceQty
		od["customer_compound"]=d.CustomerCpd

		if d.OrderType!="": od["order_type"]=d.OrderType
		if not(d.DeliveryDate_v is None): od["delivery_date"]=d.DeliveryDate_v.strftime("%Y-%m-%d %H:%M:%S")
		if not(d.DeliveryConfirmation is None): od["delivery_confirm_date"]=d.DeliveryConfirmation.strftime("%Y-%m-%d %H:%M:%S")
		if not(d.OldConfirmDate is None): od["delivery_confirm_date_old"]=d.OldConfirmDate.strftime("%Y-%m-%d %H:%M:%S")
		if not(d.EstimatedshippingDate is None): od["estimate_shipping_date"]=d.EstimatedshippingDate.strftime("%Y-%m-%d %H:%M:%S")
		print(od)
		o_details.append(od)	

		#print(o_details)
		if len(o_details)>0:
			models.execute_kw(db, uid, password, 'sale.order.line', 'create',[o_details])
	
	#--End Details

	#Ko co loi thi insert danh dau da import ok
	if count_error==0:
		cmdIns = connSQL.cursor()
		cmdIns.execute("Insert Into odoo_ImportedOrder(OrderID) \
						Values ('"+ d.OrderID +"')")
		cmdIns.commit()
		cmdIns.close()
		#models.execute_kw(db, uid, password, 'sale.order.line', 'create',[{'order_id':order_id,'line_no':'01','product_id': 58, 'product_uom_qty': 14}])    
#print(rows)
curs.close()
quit()

