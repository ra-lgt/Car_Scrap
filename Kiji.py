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


class Kiji:
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
                        print("number",i)

                        self.wait.until(EC.presence_of_element_located((By.ID,element))).send_keys(data)
                return
    
            except Exception as e:
                self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Error : Error locating element"))
                self.logs.increment_value_in_file("ERROR.txt")
                print(e)
                time.sleep(1)
                i+=1
    
    def get_item_details(self):
        self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Info : Getting next details"))
        i=0
        data={}
        flag=False
        while(i<5):
            try:
                print("dataaa",data)
                data['ad_id']=self.wait.until(EC.presence_of_element_located((By.CLASS_NAME,'adId-1017171818'))).text
                data['car_name']=self.wait.until(EC.presence_of_element_located((By.CLASS_NAME,'title-4206718449'))).text
                data['price']=self.wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="ViewItemPage"]/div[5]/div/div/div[1]/div/span/span[1]'))).text
                data['broker_name']=self.wait.until(EC.presence_of_element_located((By.CLASS_NAME,'profileName-209031168'))).text
                phone=self.wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vip-body"]/div[5]/div[2]/div[2]/div/button')))

                if(phone):
                    flag=True
                    print("PHONE")
                    phone.click()
                    data['number']=self.wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vip-body"]/div[5]/div[2]/div[2]/div/a'))).get_attribute('aria-label')
                else:
                    print("else comming")
                    break
                break
            except:
                self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Info : Phone number is not found"))
                self.logs.increment_value_in_file("SUCCESS.txt")
                if(data['ad_id'] and data['car_name'] and data['price'] and data['broker_name']):
                    break
                i+=1
        print(data)
        if(flag==True):
            self.thresh_kiji+=1
            self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Success : Phone number found"))
            self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Success : Pushing data to excel"))
            self.logs.increment_value_in_file("SUCCESS.txt")

            self.push_data_to_excel(data)

    def push_data_to_excel(self,data):
        if(not Data_push.check_id(data['ad_id'],"Kijiji")):
            Data_push.push_data(data,"Kijiji")
        self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Success : Successfully added the data"))
        self.logs.increment_value_in_file("SUCCESS.txt")
        

    def initial_setup(self):    
        location=WebDriverWait(self.driver,5).until(
            EC.presence_of_element_located((By.ID,"SearchLocationPicker"))
        )
        location.click()
        time.sleep(1)
        
        location_text=WebDriverWait(self.driver,5).until(
            EC.presence_of_element_located((By.ID,"SearchLocationSelector-input"))
        )
        location_text.send_keys("canada")
        time.sleep(self.sleep//3)
        
        location_text.send_keys(Keys.ENTER)
        time.sleep(self.sleep)
        
        self.driver.get("https://www.kijiji.ca/")
    
    def get_batch_details(self):
        pass

    
    def get_name_number(self):
        self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Fetching the data"))
        ul_element = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="base-layout-main-wrapper"]/div[4]/div[4]/div[2]/div[3]/ul')))
        li_elements = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="base-layout-main-wrapper"]/div[4]/div[4]/div[2]/div[3]/ul/li')))
        

        for li in li_elements:
            if(self.thresh_kiji>=self.thresh):
                self.exit=True
                return

            try:
                a_tag=li.find_element(By.XPATH, './section/div[1]/div[2]/div[1]/h3/a').get_attribute("href")
                self.driver.execute_script("window.open('" + a_tag +"');")
                self.driver.switch_to.window(self.driver.window_handles[-1])
                self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Success : Successfully targetted the element"))
                self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Info : No. of Data Looked up :{}".format(self.thresh)))
                self.logs.increment_value_in_file("SUCCESS.txt")

                self.get_item_details()
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[0])
            except:
                self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Error : Error getting the data"))
                self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Error : Retrying....."))
                self.logs.increment_value_in_file("ERROR.txt")
                continue
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="base-layout-main-wrapper"]/div[4]/div[4]/div[2]/div[3]/div[3]/div[1]/nav/ul/li[6]/a'))).click()
        time.sleep(self.sleep)
        self.driver.refresh()
        time.sleep(self.sleep+5)

        self.get_name_number()


    
    def scrap_car(self):
        time.sleep(self.sleep)
        
        
        self.repeat_search('//*[@id="autosSearchForm"]/div[2]/button',"XPATH",{"event":"click"})
        time.sleep(1)
        self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Info : Setting the Year min 1975"))


                
        self.repeat_search('caryear_min',"ID",{"event":"send"},1975)
        time.sleep(1)
        # from_year=self.wait.until(EC.presence_of_element_located((By.ID,'caryear_min')))
        current_year = datetime.now().year
        self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Info : Setting the current year as max"))

        self.repeat_search('caryear_max',"ID",{"event":"send"},current_year)
        time.sleep(1)
        
        # self.wait.until(EC.presence_of_element_located((By.ID,'caryear_max'))).send_keys(current_year)
        self.repeat_search('//*[@id="accordion__panel-caryear"]/div/div[2]/button',"XPATH",{"event":"click"})
        time.sleep(self.sleep)
        self.repeat_search('//*[@id="accordion__heading-forsaleby"]',"XPATH",{"event":"click"})
        time.sleep(self.sleep//2)
        self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Info : Setting the for sale by owner"))
        self.repeat_search('//*[@id="forsaleby-ownr"]',"XPATH",{"event":"click"})
        time.sleep(self.sleep//3)

        self.get_name_number()
    
    def scrap_bike(self):
        time.sleep(self.sleep//2)
        self.repeat_search('//*[@id="accordion__heading-forsaleby"]',"XPATH",{"event":"click"})
        time.sleep(self.sleep//2)
        self.repeat_search('//*[@id="forsaleby-ownr"]',"XPATH",{"event":"click"})
        time.sleep(self.sleep//2)
        self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Info : Setting the for sale by owner"))

        self.repeat_search('//*[@id="accordion__heading-caryear"]',"XPATH",{"event":"click"})

        self.repeat_search('caryear_min',"ID",{"event":"send"},1975)
        self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Info : Setting the Year min 1975"))
        time.sleep(self.sleep//3)
        current_year = datetime.now().year

        self.repeat_search('caryear_max',"ID",{"event":"send"},current_year)
        time.sleep(self.sleep//3)
        self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Info : Setting the current year as max"))
        
        self.repeat_search('//*[@id="accordion__panel-caryear"]/div/div[2]/button',"XPATH",{"event":"click"})

        self.get_name_number()
    
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
        self.driver.implicitly_wait(10)
        go_btn=WebDriverWait(self.driver,self.sleep//2).until(
            EC.presence_of_element_located((By.ID,"LocUpdate"))
        )
        
        if(go_btn):
            self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Info : Making the intitial setup"))
            self.initial_setup()
            self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Info : intitial setup done"))
            
        if(self.choice=="Cars/Trucks"):
            car_element = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="Columns"]/main/section[3]/div[2]/div/div[2]/a')))
            car_element.click()
            self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Info : Scrapping the car data"))
            self.scrap_car()
        
        elif(self.choice=="Bike"):
            bike_element=self.wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="Columns"]/main/section[3]/div[2]/div/div[6]/a')))
            bike_element.click()
            self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Info : Scrapping the bike data"))
            self.scrap_bike()
