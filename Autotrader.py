from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import Data_push
from Logs import Logs
from urllib.parse import urlparse


class Autotrader:
    @property
    def now(self):
        return datetime.now()
    
    def __init__(self,url=None,choice=None,sleep=0,threshold=0,browser="Headless"):
        self.choice=choice
        self.final_data=[]
        self.li_batch=[]
        self.url=url
        self.kiji_sucess=0
        self.driver=None
        self.sleep=sleep
        self.thresh=threshold
        self.thresh_kiji=0
        self.logs=Logs()
        self.browser=browser
        self.exit=False
        self.kind=""
        self.page=15
        
    def repeat_search(self,element,type,action,data=None):
        
        i=0
        while(i<5):
            time.sleep(1)
            try:
                if(type=="XPATH"):
                    if(action["event"]=="click"):
                        print("clickkk")
                        self.wait.until(EC.presence_of_element_located((By.XPATH,element))).click()
                elif(type=="ID"):
                    if(action['event']=="send"):

                        self.wait.until(EC.presence_of_element_located((By.ID,element))).send_keys(data)
                    elif(action['event']=="element"):
                        self.wait.until(EC.presence_of_element_located((By.ID,element)))
                return
    
            except Exception as e:
                self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Error : Error locating element"))
                self.logs.increment_value_in_file("ERROR.txt")
                print(e)
                time.sleep(1)
                i+=1
                
    def get_item_details(self):
        self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Info : Element targetted successfully"))  
        self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Info : Fetching data"))  
        data={}
        flag=False
        try:
            self.driver.execute_script("window.scrollBy({ top: 290, behavior: 'smooth' });" )
            time.sleep(self.sleep//3)

            
            href = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".link.ng-star-inserted")))
            href.click()
            time.sleep(self.sleep//2)
            
            url = self.driver.current_url
            parsed_url = urlparse(url)
            data['ad_id'] = parsed_url.path.split('/')[-2]
            data['vehicle_name']=self.wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="heroTitleWrapper"]/h1'))).text
            data['price']=self.wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="heroWrapperDescription"]/div[2]/div/div[1]/div/p[2]'))).text
            data['dealer_name']=self.wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="privateLeadContainer"]/vdp-private-lead-header/div[1]/div/p'))).text
            data['number']=self.wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="privateLeadContainer"]/vdp-private-lead-header/div[2]/div[2]/vdp-private-lead-phone/div/div/p'))).text
            flag=True
        except Exception as e:
            self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Info : Phone number not found"))
            self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Info : Moving to next data"))    
            pass
            #https://www.autotrader.ca/a/honda/hr-v/saint-jean-sur-richelieu/quebec/19_12765798_/?showcpo=ShowCpo&ncse=no&ursrc=pl&urp=7&urm=8&pc=M5V%203L9&sprx=-1
        if(flag==True):
            self.thresh_kiji+=1
            self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Success : Phone number found"))
            self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Success : Pushing data to excel"))
            self.logs.increment_value_in_file("SUCCESS.txt")
            print("SUCCESS")
            self.push_data_to_excel(data)
        print("DATA:",data)

        
    
    def push_data_to_excel(self,data):
        if(not Data_push.check_id(data['ad_id'],self.kind)):
            Data_push.push_data(data,self.kind)
            print("hekkollllll")
        self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Success : Successfully added the data"))
        self.logs.increment_value_in_file("SUCCESS.txt")
        
    
    def car_scrap(self):
        time.sleep(self.sleep)
        car_list=self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'.col-xs-12.result-item.enhanced')))
        self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Info : Scarpping started"))  
        for car in car_list:
            try:
                time.sleep(self.sleep//2)
                href_car=car.find_element(By.CSS_SELECTOR,".inner-link")
                self.driver.execute_script("arguments[0].scrollIntoView();", href_car)
                href_tag=href_car.get_attribute("href")
                self.driver.execute_script("window.open('" + href_tag +"');")
                self.driver.switch_to.window(self.driver.window_handles[-1])
                time.sleep(self.sleep//2)
                self.get_item_details()
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[0])
            except:
                self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Info : Missed retrying"))  
        self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Info : Moving to next page"))  
        next=self.wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="listingsPagerWrapper"]/div/div/ul/li[8]/a')))
        next.click()
        self.car_scrap()
        
        
    def bike_scrap(self):
        time.sleep(self.sleep)
        bike_list=self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'.col-xs-12.result-item')))
        self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Info : Scarpping started"))  
        for bike in bike_list:
            try:
                if(self.thresh_kiji>=self.thresh):
                    self.exit=True
                    return
                time.sleep(self.sleep//2)
                href_bike=bike.find_element(By.CSS_SELECTOR,'.result-title.click')
                self.driver.execute_script("arguments[0].scrollIntoView();", href_bike)
                href_tag=href_bike.get_attribute("href")
                self.driver.execute_script("window.open('" + href_tag +"');")
                self.driver.switch_to.window(self.driver.window_handles[-1])
                time.sleep(self.sleep//2)
                self.get_item_details()
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[0])
            except:
                pass
        self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Info : Moving to next page"))  
        self.driver.get("https://www.autotrader.ca/motorcycles-atvs/all/?rcp=15&rcs={}&srt=9&yRng=1976%2C&prx=-1&loc=M5V%203L9&hprc=False&wcp=False&sts=New-Used&adtype=Private&showcpo=1&inMarket=advancedSearch".format(self.page))
        self.page+=15
        self.bike_scrap()
        
        
        
        #https://www.autotrader.ca/motorcycles-atvs/all/?rcp=15&rcs=0&srt=9&yRng=1976%2C&prx=-1&loc=M5V%203L9&hprc=False&wcp=False&sts=New-Used&adtype=Private&showcpo=1&inMarket=advancedSearch
    #https://www.autotrader.ca/motorcycles-atvs/all/?rcp=15&rcs=45&srt=9&yRng=1976%2C&prx=-1&loc=M5V%203L9&hprc=False&wcp=False&sts=New-Used&adtype=Private&showcpo=1&inMarket=advancedSearch    
    
    def start_scrap(self):
            
        self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Info : Starting the Scrapping process"))
        
        options = Options()

        options.page_load_strategy ="eager"
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        if(self.browser=="Headless"):
            options.add_argument("--headless")
            options.add_argument("--window-size=1920,1080")

        self.driver = webdriver.Chrome(options=options)
        self.wait=WebDriverWait(self.driver, self.sleep//2)
        self.driver.get(self.url)
        self.driver.implicitly_wait(20)
        self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Info :Zip Code Updated"))
        self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Info : min year updated to 1975"))
        self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Info : Max year to max year"))
        self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Info : data sorted"))
        self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Info : setting ownership"))  
        if(self.choice=="Cars/Trucks"):
            self.kind="Autotrader_cars"
            self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Info : Start Scrapping car data"))  
            self.car_scrap()
        else:
            self.kind="Autotrader_bikes"
            self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Info : Start Scrapping bike data"))  
            self.bike_scrap()
        
        
        