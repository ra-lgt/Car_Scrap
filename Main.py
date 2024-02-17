from Kiji import Kiji
from Kiji_Auto import Kiji_Auto



class Main:
    def start_scrap(self,url,type,choice=None):
        if(type=="Kiji"):
            Kiji(url,choice)
        
        elif(type=="Kiji_auto"):
            Kiji_Auto(url)
        else:
            pass

main=Main()
main.start_scrap("https://www.kijijiautos.ca/","Kiji_auto")


