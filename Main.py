from Kiji import Kiji
from Kiji_Auto import Kiji_Auto
import multiprocessing
import time
from datetime import datetime
from Logs import Logs
from Autotrader import Autotrader
class Main(Autotrader):
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
        self.kiji=Autotrader()
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

    
    def backend_app(self,threshold,sleep,browser,car_bike):
        if(car_bike=="Cars/Trucks"):
            self.start_scrap(url="https://www.autotrader.ca/cars/?rcp=15&rcs=0&srt=9&yRng=1975%2C&prx=-1&loc=M5V%203L9&hprc=True&wcp=True&sts=New-Used&adtype=Private&inMarket=advancedSearch",choice=car_bike,sleep=sleep,threshold=threshold,browser=browser)
        elif(car_bike=="Bike"):
            
            self.start_scrap(url="https://www.autotrader.ca/motorcycles-atvs/all/?rcp=15&rcs=0&srt=9&yRng=1976%2C&prx=-1&loc=M5V%203L9&hprc=False&wcp=False&sts=New-Used&adtype=Private&showcpo=1&inMarket=advancedSearch",sleep=sleep,threshold=threshold,browser=browser)

        print(type,threshold,sleep)

    
        
    def start_scrap(self,url,choice=None,sleep=0,threshold=0,browser="Headless"):
        if(True):

            while(True):
                if(self.kiji.exit):
                        break
                if(self.logs.get_value_from_file("ERROR.txt")>=threshold//10 or self.first_kiji or self.logs.get_value_from_file("SUCCESS.txt")==0 or self.logs.get_value_from_file("ERROR.txt")>10*self.logs.get_value_from_file("SUCCESS.txt")):       
                    if(self.process):
                        self.process.terminate()
                        self.kiji.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Killing the Old thread"))
                    self.kiji.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Starting the new thread"))
                    
                    kiji_instance=Autotrader(url=url,choice=choice,sleep=sleep,threshold=threshold,browser=browser)
                    self.process = multiprocessing.Process(target=kiji_instance.start_scrap)
                    self.process.start()
                    self.first_kiji=False
                    if(self.kiji.exit):
                        break
                else:
                    pass
                self.sleepy()
    

# if __name__=="__main__":
#     main=Main()
#     main.start_scrap("https://kijiji.ca/","Kiji","cars")


