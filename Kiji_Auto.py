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
from urllib.parse import urlparse, parse_qs
import pandas as pd
from selenium.webdriver import ActionChains
from openpyxl import load_workbook
import Data_push
from datetime import datetime
from Logs import Logs



class Kiji_Auto:
    @property
    def now(self):
        return datetime.now()

    def __init__(self,url=None,sleep_auto=0,thresh_auto=0,browser="Headless"):
        super().__init__()
        self.driver=None
        self.url=url
        self.final_data=[]
        self.sleep_auto=sleep_auto
        self.thresh_auto=thresh_auto
        self.kiji_auto_thersh=0
        self.logs=Logs()
        self.browser=browser
        self.exit=False
        # self.start_scrap()
    
    def repeat_search(self,element,type,action):
        i=0
        while(i<5):
            try:
                if(type=="XPATH"):
                    if(action=="click"):
                        self.wait.until(EC.presence_of_element_located((By.XPATH,element))).click()
                    elif(action=="data"):
                        self.wait.until(EC.presence_of_element_located((By.XPATH,element)))
                elif(type=="CLASS"):
                    if(action=="click"):
                        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME,element))).click()
                elif(type=="ID"):
                    if(action=="click"):
                        self.wait.until(EC.presence_of_element_located((By.ID,element))).click()
                self.logs.increment_value_in_file("SUCCESS.txt")

                break
            except:
                self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Error : Error locating element"))
                self.logs.increment_value_in_file("ERROR.txt")
                i+=1
    def get_item_details(self):
        self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Info : Getting the vehicle details"))
        i=0
        data={}
        flag=False
        while(i<5):
            
            try:
                time.sleep(self.sleep_auto//2)
                mobile_btn=self.wait.until(EC.presence_of_element_located((By.XPATH,'//*[@data-testid="PhoneRevealButton"]')))
                if(mobile_btn):
                    flag=True
                mobile_btn.click()
                time.sleep(self.sleep_auto//3)


                
                url = self.driver.current_url
                parsed_url = urlparse(url)
                data['ad_id']=[parsed_url.fragment[4:]]
                
                data['car_name']=[self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.G2jAym.g3zFtQ.D2jAym.p2jAym.b2jAym'))).text]
                data['price']=[self.wait.until(EC.presence_of_element_located((By.XPATH,'//*[@data-testid="listing-basic-info-section-price"]'))).text]
                data['dealer_name']=[self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.G2jAym.C2jAym.p2jAym.b2jAym'))).text]
                data['mobile']=[self.wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="root"]/div[3]/section/div/div/div[1]/div[1]/div[3]/span'))).text]
                self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Info : Data has Number and adding to the excel"))
                print("DATA ADDED")
                self.kiji_auto_thersh+=1
                return data

                
            except:
                self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Info : Cannot find Mobile number"))
                self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"info : Moving to Next Data"))
                if(flag==False):
                    return data
                print("DATA ERROR")
                i+=1
        
        return data
    
    def push_data_to_excel(self,data):
        if(not Data_push.check_id(data['ad_id'],"Kijiji_Autos")):
            Data_push.push_data(data,"Kijiji_Autos")
        self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Success : Data pushed to the excel"))


                
    def get_list_cars(self):
        time.sleep(self.sleep_auto//2)
        index=0
        while(True):
            time.sleep(self.sleep_auto//3)
            ul_list = self.wait.until(EC.presence_of_element_located((By.XPATH, "//*[@data-testid='ListItemPage-{}']".format(index))))
            li_list = ul_list.find_elements(By.TAG_NAME, 'article')
            size=1
            print("-"*100)
            print("ul_list")
            for li in li_list:
                print("li_list")
                if(self.kiji_auto_thersh>=self.thresh_auto):
                    self.exit=True
                    return
                car_data={}
                i=0

                self.driver.execute_script("window.scrollBy({ top: 290, behavior: 'smooth' });" )
                time.sleep(self.sleep_auto//2)
                self.driver.execute_script("window.scrollBy({ top: -75, behavior: 'smooth' });")
                time.sleep(self.sleep_auto//2)

                while(i<5):
                    try:
                        time.sleep(2)

                        href=li.find_element(By.CSS_SELECTOR,'a.bcNN7t').get_attribute("href")

                        self.driver.execute_script("window.open('" + href +"');")
                        self.driver.switch_to.window(self.driver.window_handles[-1])
                        self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Success : Successfully targeted the element"))
                        self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Info : No. of Data Looked up :{}".format(self.kiji_auto_thersh)))
                        car_data=self.get_item_details()
                        self.driver.close()
                        self.driver.switch_to.window(self.driver.window_handles[0])
                        self.logs.increment_value_in_file("SUCCESS.txt")
                        break
                    except:
                        self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Error : Error in getting data"))
                        self.logs.increment_value_in_file("ERROR.txt")
                        i+=1
                if(car_data):
                    self.push_data_to_excel(car_data)
                size+=1
                print(size)
                time.sleep(self.sleep_auto//2)
            index+=1
                

    def start_scrap(self):
        options = Options()
        if(self.browser=="Headless"):
            options.add_argument("--headless")
            options.add_argument("--window-size=1920,1080")
        options.page_load_strategy ="eager"
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(self.url)
        self.driver.implicitly_wait(10)
        self.wait=WebDriverWait(self.driver, self.sleep_auto)
        time.sleep(self.sleep_auto//2)
        self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Info : Kijiji Auto Scarpping Started"))

        self.repeat_search("//*[@id='root']/div[3]/div[2]/section[1]/div/div/div[2]/form/footer/button[2]","XPATH","click")
        time.sleep(self.sleep_auto//3)
        self.repeat_search("//*[@id='root']/div[3]/div/section[5]/div/div/div[1]/div/ul/li[2]/button","XPATH","click")
        time.sleep(self.sleep_auto//3)
        self.repeat_search("//*[@id='CONSTRUCTION_YEAR-from']","XPATH","click")
        self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Info : Setting the Year min 1975"))
        time.sleep(self.sleep_auto//3)
        self.repeat_search("//*[@id='CONSTRUCTION_YEAR']/fieldset/div/div[1]/div/ul/li[40]","XPATH","click")
        self.repeat_search("//*[@id='CONSTRUCTION_YEAR-to']","XPATH","click")
        self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Info : Setting the Year max current year"))
        time.sleep(self.sleep_auto//3)
        self.repeat_search("//*[@id='CONSTRUCTION_YEAR']/fieldset/div/div[3]/div/ul/li[3]","XPATH","click")
        time.sleep(self.sleep_auto//3)
        self.repeat_search("//*[@data-testid='FilterModalButtonBarSubmit']","XPATH","click")
        time.sleep(self.sleep_auto//3)
        self.repeat_search("//*[@id='root']/div[3]/div/section[5]/div/div/div[1]/div/ul/li[10]/button","XPATH","click")
        time.sleep(self.sleep_auto//3)
        # self.wait.until(EC.presence_of_element_located((By.ID,'st-private_seller'))).click()
        self.repeat_search("//*[@id='SELLER_TYPE']/fieldset/label[2]/span[1]","XPATH","click")

        self.wait.until(EC.presence_of_element_located((By.XPATH,'//*[@data-testid="FilterModalButtonBarSubmit"]'))).click()
        time.sleep(self.sleep_auto//3)
        self.wait.until(EC.presence_of_element_located((By.XPATH,'//*[@data-testid="sortOrder"]'))).click()

        self.wait.until(EC.presence_of_element_located((By.XPATH,'//*[@data-value="DATE_CREATED:DESC"]'))).click()
        self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Info : Setting sorting to most recent"))
        self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Info : Started to get the data"))

        self.get_list_cars()


        
        
