from Kiji import Kiji




class Main:
    def start_scrap(self,url,type,choice):
        if(type=="Kiji"):
            Kiji(url,choice)
        
        elif(type=="Kiji_auto"):
            pass
        else:
            pass

main=Main()
main.start_scrap("https://www.kijiji.ca/","Kiji","cars")


