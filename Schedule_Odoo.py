import sched, time
from Update_OrderDetails import *

s = sched.scheduler(time.time, time.sleep)

def print_time(a='default'):
	#print("Runing On Time:", time.time(), a)
	print("Runing.... (Syn Order Details)")
	Update_OrderDetail_To_odoo()
    

def scheduler_run():
    print('Press CTRL+C to stop') 
    #i=0
	#print('')
    try: 
        while True: 
            s.enter(30, 0,print_time)
            print("waiting....")
            
            #s.enter(10, 0, print_time, argument=('positional',))
            #s.enter(15, 0, print_time, kwargs={'a': 'keyword'})        	
            #i=i+1
            s.run()
    #Stopping when CTRL+C is pressed 
    except KeyboardInterrupt: 
          print("End....")



scheduler_run()
#Update_OrderDetail_To_odoo()


