import logging
import time
import xmlrpc.client
import pyodbc

def Update_OrderDetail_To_odoo():	
	logging.basicConfig(filename='LogError.log', level=logging.INFO,format='%(asctime)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
	#---------- Update Odoo -----------------
	url="https://tuico:tsxs9cp3yP3MJHYq@erp.tuicovn.com"
	username="synchdata@tuicovn.com"
	password="dtSynxgad2!~od321"
	db="tuico_live"

	common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
	uid = common.authenticate(db, username, password, {})

	if uid ==0:		
		logging.error('Dang nhap sai')
		quit()	
	models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

	forkey=""
	lsUpd=[]
	#------------*****  SQL Server  *****----------
	connSQL = pyodbc.connect('Driver={SQL Server};'
	                      'Server=192.168.0.1;'
	                      'Database=O-Ring Material;'
	                      'uid=sa;pwd=356112342597')
	SqlRs = connSQL.cursor()
	#SqlRs.execute("Select top 100 OrderDetail_IDD, TblName, odoo_id, Compound, BeginQC, FinishQC, MoldOn, MoldOff,forkey \
	#				From Odoo_vwOrderDetails_NeedUpdateOdd Where OdooUpdated is not null Order By forkey")
	SqlRs.execute("Select OrderDetail_IDD, TblName, odoo_id, Compound, BeginQC, FinishQC, MoldOn, MoldOff,forkey \
					From Odoo_vwOrderDetails_NeedUpdateOdd Order By forkey")

	for rowSQL in SqlRs:
		if forkey!=rowSQL[8]:
			print(rowSQL[8])
			forkey=rowSQL[8]
		#print(rowSQL)	
		OD_dict={}
		id=rowSQL[2] #odoo_id
		compound=rowSQL[3].strip()	
		#print(compound)
		if compound!='':
			ids=models.execute_kw(db, uid, password,
				    'product.product', 'search',
				    [[['default_code', 'ilike',compound]]])
			if len(ids)==0:
				#print("ko tim thay compound")
				CpdItem={}
				CpdItem["default_code"]=compound
				CpdItem["name"]=compound
				CpdItem["tuico_product_type"] ='compound'
				CpdItem["type"] ='product'
				CpdItem["uom_id"] =3 #kg
				CpdItem["hs_code"]='Auto Synch'
				#print(CpdItem)
				try :
					idCpd = models.execute_kw(db, uid, password, 'product.product', 'create', [CpdItem])
				except:
					errDes="Error: Insert Cpd: "+compound
					print(errDes);
					logging.error(errDes)				
			else:
				idCpd=ids[0]
			OD_dict["compound_id"] = idCpd
		else:
			OD_dict["compound_id"] = False
		
		OD_dict["begin_qc_date"] = rowSQL[4]
		OD_dict["finish_qc_date"] = rowSQL[5]
		OD_dict["mold_on"] = rowSQL[6]
		OD_dict["mold_off"] = rowSQL[7]
		#print(OD_dict)
		try :
			models.execute_kw(db, uid, password, 'sale.order.line', 'write', [[id],OD_dict])
			Upd={}
			Upd["OrderDetail_IDD"]=rowSQL[0]
			Upd["TblName"]=rowSQL[1]
			lsUpd.append(Upd)			
			#print(lsUpd)
		except:
			errDes="Error: Insert Order Details ID:"+rowSQL[0] + " Table: "+rowSQL[1] 
			print(errDes);
			logging.error(errDes)

	SqlRs.close()
	SqlCmd = connSQL.cursor()
	for r in lsUpd:		
		sql="Delete From odoo_OrderDetail_Updated Where OrderDetail_IDD="+str(r["OrderDetail_IDD"])+" And TblName='" + r["TblName"] + "'"
		SqlCmd.execute(sql)
		#print(sql)		
	connSQL.commit()

		
		#print(sql)
#print(id)
#quit()	

"""
OD_dict={}
OD_dict["compound_id"] =False
OD_dict["mold_off"] = ""
#print(OD_dict)
#quit()

"""

