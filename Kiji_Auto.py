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


class Kiji_Auto:
    def __init__(self,url):
        options = Options()
        options.page_load_strategy ="eager"
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(url)
        self.driver.implicitly_wait(10)
        self.wait=WebDriverWait(self.driver, 10)
        self.final_data=[]
        self.start_scrap()
    def repeat_search(self,element,type,action):
        i=0
        while(i<5):
            try:
                if(type=="XPATH"):
                    if(action=="click"):
                        self.wait.until(EC.presence_of_element_located((By.XPATH,element))).click()
                elif(type=="CLASS"):
                    if(action=="click"):
                        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME,element))).click()
                elif(type=="ID"):
                    if(action=="click"):
                        self.wait.until(EC.presence_of_element_located((By.ID,element))).click()

                break
            except:
                print("ERROR")
                i+=1
    

    def start_scrap(self):
        time.sleep(5)

        self.repeat_search("//*[@id='root']/div[3]/div[2]/section[1]/div/div/div[2]/form/footer/button[2]","XPATH","click")
        time.sleep(3)
        self.repeat_search("//*[@id='root']/div[3]/div/section[5]/div/div/div[1]/div/ul/li[2]/button","XPATH","click")
        time.sleep(3)
        self.repeat_search("//*[@id='CONSTRUCTION_YEAR-from']","XPATH","click")
        time.sleep(3)
        self.repeat_search("//*[@id='CONSTRUCTION_YEAR']/fieldset/div/div[1]/div/ul/li[32]","XPATH","click")
        self.repeat_search("//*[@id='CONSTRUCTION_YEAR-to']","XPATH","click")
        time.sleep(3)
        self.repeat_search("//*[@id='CONSTRUCTION_YEAR']/fieldset/div/div[3]/div/ul/li[3]","XPATH","click")
        time.sleep(3)
        self.repeat_search("//*[@data-testid='FilterModalButtonBarSubmit']","XPATH","click")
        time.sleep(3)
        self.repeat_search("//*[@id='root']/div[3]/div/section[5]/div/div/div[1]/div/ul/li[10]/button","XPATH","click")
        time.sleep(3)
        # self.wait.until(EC.presence_of_element_located((By.ID,'st-private_seller'))).click()
        self.repeat_search("//*[@id='SELLER_TYPE']/fieldset/label[1]/span[1]","XPATH","click")

        self.wait.until(EC.presence_of_element_located((By.XPATH,'//*[@data-testid="FilterModalButtonBarSubmit"]'))).click()
        
        import pdb;pdb.set_trace()
        
