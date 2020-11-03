import sched, time
s = sched.scheduler(time.time, time.sleep)

def print_time(a='default'):
     print("From print_time", time.time(), a)

def scheduler_run():
     print("Press ENTER to count laps.\nPress CTRL+C to stop") 
     print("")
     i=1
     try: 
          while True: 
               s.enter(5, 0, print_time)
               s.enter(10, 0, print_time, argument=('positional',))
               s.enter(15, 0, print_time, kwargs={'a': 'keyword'})

               print(i)
               #print(time.time())
               s.run()
               i=i+1
     #Stopping when CTRL+C is pressed 
     except KeyboardInterrupt: 
          print("Done")


scheduler_run()

