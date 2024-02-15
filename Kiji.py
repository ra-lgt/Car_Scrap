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



class Kiji:
    def __init__(self,url,choice):
        self.choice=choice
        options = Options()
        options.page_load_strategy = 'eager'
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(url)
        self.driver.implicitly_wait(10)
        self.wait=WebDriverWait(self.driver, 20)
        
        
        self.start_scrap()
        
    def repeat_search(self,element):
        i=0
        while(i<5):
            try:
                search_btn=self.wait.until(EC.presence_of_element_located((By.XPATH,element)))
        
                search_btn.click()
            
            except:
                i+=1
        
    
    def initial_setup(self):    
        location=WebDriverWait(self.driver,5).until(
            EC.presence_of_element_located((By.ID,"SearchLocationPicker"))
        )
        location.click()
        
        location_text=WebDriverWait(self.driver,5).until(
            EC.presence_of_element_located((By.ID,"SearchLocationSelector-input"))
        )
        location_text.send_keys("canada")
        time.sleep(3)
        
        location_text.send_keys(Keys.ENTER)
        time.sleep(10)
        
        self.driver.get("https://www.kijiji.ca/")
    
    def scrap_car(self):
        
        self.repeat_search('//*[@id="autosSearchForm"]/div[2]/button')
                
        
        from_year=self.wait.until(EC.presence_of_element_located((By.ID,'caryear_min')))
        from_year.send_keys("1975")
        current_year = datetime.now().year
        
        self.wait.until(EC.presence_of_element_located((By.ID,'caryear_max'))).send_keys(current_year)
        self.wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="accordion__panel-caryear"]/div/div[2]/button'))).click()
        self.wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="base-layout-main-wrapper"]/div[4]/div[4]/div[1]/div[1]/div/div[15]'))).click()
        time.sleep(3)
        self.wait.until(EC.presence_of_element_located((By.ID,'forsaleby-ownr'))).click()
    
    def start_scrap(self):
        go_btn=WebDriverWait(self.driver,5).until(
            EC.presence_of_element_located((By.ID,"LocUpdate"))
        )
        
        if(go_btn):
            self.initial_setup()
            
        if(self.choice=="cars"):
            car_element = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="Columns"]/main/section[3]/div[2]/div/div[2]/a')))
            car_element.click()
            self.scrap_car()
        
        elif(self.choice=="bike"):
            bike_element=self.wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="Columns"]/main/section[3]/div[2]/div/div[6]/a')))
            bike_element.click()
        import pdb;pdb.set_trace()