import pandas as pd
from datetime import datetime
import Google_sheet
import threading

def push_data(data,name):
    data_to_append=pd.DataFrame(data,index=[0])

    if(name=="Autotrader_cars"):
        create_kiji_auto_id(data)
        thread = threading.Thread(target=Google_sheet.push_data, args=(data, "Autotrader_cars"))
        thread.start()
        # Google_sheet.push_data(data=data,name="Kijiji_Auto_Data")
    elif(name=="Autotrader_bikes"):
        create_kiji_ids(data)
        thread = threading.Thread(target=Google_sheet.push_data, args=(data, "Autotrader_bikes"))
        thread.start()
        # Google_sheet.push_data(data=data,name="Kijiji_Data")


    excel_file_path = '{}.xlsx'.format(name)
    try:
        existing_data = pd.read_excel(excel_file_path)

        combined_data = pd.concat([existing_data, data_to_append], ignore_index=True)

        
    except FileNotFoundError:
        combined_data = data_to_append
        
    try:
        combined_data.to_excel(excel_file_path, index=False)
    except:
        pass

def create_kiji_auto_id(data):
    ids={}
    ids['ad_id']=data['ad_id']
    data_to_append=pd.DataFrame(ids,index=[0])
    excel_file_path = '{}_ids.xlsx'.format("Autotrader_cars")

    try:
        existing_data = pd.read_excel(excel_file_path)

        combined_data = pd.concat([existing_data, data_to_append], ignore_index=True)

        
    except FileNotFoundError:
        combined_data = data_to_append
    try:
        combined_data.to_excel(excel_file_path, index=False)
    except:
        pass

def create_kiji_ids(data):
    ids={}
    ids['ad_id']=data['ad_id']
    data_to_append=pd.DataFrame(ids,index=[0])
    excel_file_path = '{}_ids.xlsx'.format("Autotrader_bikes")

    try:
        existing_data = pd.read_excel(excel_file_path)

        combined_data = pd.concat([existing_data, data_to_append], ignore_index=True)

        
    except FileNotFoundError:
        combined_data = data_to_append
        
    try:
        combined_data.to_excel(excel_file_path, index=False)
    except:
        pass

def check_id(id,type):
    xl=None
    try:
        if(type=="Autotrader_cars"):
            xl = pd.ExcelFile('Autotrader_cars_ids.xlsx')
        elif(type=="Autotrader_bikes"):
            xl = pd.ExcelFile('Autotrader_bikes_id.xlsx')
        df = xl.parse('Sheet1')

        if id in df['ad_id'].values:
            return True
    except:
        return False
    return False
