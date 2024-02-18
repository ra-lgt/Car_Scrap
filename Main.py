from Kiji import Kiji
from Kiji_Auto import Kiji_Auto
import multiprocessing
import time
from datetime import datetime
from Logs import Logs
class Main(Kiji_Auto,Kiji):
    @property
    def now(self):
        return datetime.now()
    def __init__(self):
        Kiji().__init__()
        Kiji_Auto().__init__()
        self.process=None
        self.first_kiji=True
        self.first_auto=True
        self.auto_process=None
        self.kiji=Kiji()
        self.Kiji_auto=Kiji_Auto()
        self.logs=Logs()
    
    def get_log(self):
        return Kiji_Auto().logs

    def sleepy(self):
        time.sleep(900)
    
    def stop_thread(self):
        if(self.auto_process):
            self.auto_process.terminate()
        if(self.process):
            self.process.terminate()

    
    def backend_app(self,type,threshold,sleep,browser,car_bike):
        if(type=="Kiji"):
            self.start_scrap(url="https://kijiji.ca/",type="Kiji",choice=car_bike,sleep=sleep,threshold=threshold,browser=browser)
        elif(type=="Kiji_auto"):
            self.start_scrap(url="https://www.kijijiautos.ca/",type="Kiji_auto",sleep=sleep,threshold=threshold,browser=browser)

        print(type,threshold,sleep)

    
        
    def start_scrap(self,url,type,choice=None,sleep=0,threshold=0,browser="Headless"):
        if(type=="Kiji"):

            while(True):
                if(self.kiji.exit):
                        break
                if(self.logs.get_value_from_file("ERROR.txt")>=threshold//10 or self.first_kiji or self.logs.get_value_from_file("SUCCESS.txt")==0 or self.logs.get_value_from_file("ERROR.txt")>10*self.logs.get_value_from_file("SUCCESS.txt")):       
                    if(self.process):
                        self.process.terminate()
                        Kiji().logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Killing the Old thread"))
                    Kiji().logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Starting the new thread"))
                    
                    kiji_instance=Kiji(url=url,choice=choice,sleep=sleep,threshold=threshold,browser=browser)
                    self.process = multiprocessing.Process(target=kiji_instance.start_scrap)
                    self.process.start()
                    self.first_kiji=False
                    if(Kiji().exit):
                        break
                else:
                    pass
                self.sleepy()
        
        elif(type=="Kiji_auto"):
            while(True):
                if(self.Kiji_auto.exit):
                    break
                if(self.logs.get_value_from_file("ERROR.txt")>=threshold//2 or self.first_auto or self.logs.get_value_from_file("SUCCESS.txt")==0 or self.logs.get_value_from_file("ERROR.txt")>10*self.logs.get_value_from_file("SUCCESS.txt")):
                    
                    print("Thread start")
                    Kiji_Auto(url)
                    if(self.auto_process):
                        self.auto_process.terminate()
                        Kiji_Auto().logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Killing the old thread"))
                    Kiji_Auto().logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Starting the new thread"))
                    kiji_auto=Kiji_Auto(url=url,sleep_auto=sleep,thresh_auto=threshold,browser=browser)
                    self.auto_process = multiprocessing.Process(target=kiji_auto.start_scrap)
                    self.auto_process.start()
                    self.first_auto=False
                    if(Kiji_Auto().exit):
                        break

                else:
                    pass
                self.sleepy()

# if __name__=="__main__":
#     main=Main()
#     main.start_scrap("https://kijiji.ca/","Kiji","cars")


