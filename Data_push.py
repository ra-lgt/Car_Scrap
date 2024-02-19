import pandas as pd
from datetime import datetime
import Google_sheet
import threading

def push_data(data,name):
    data_to_append=pd.DataFrame(data)

    if(name=="Kijiji_Autos"):
        create_kiji_auto_id(data)
        thread = threading.Thread(target=Google_sheet.push_data, args=(data, "Kijiji_Auto_Data"))
        thread.start()
        # Google_sheet.push_data(data=data,name="Kijiji_Auto_Data")
    elif(name=="Kijiji"):
        create_kiji_ids(data)
        thread = threading.Thread(target=Google_sheet.push_data, args=(data, "Kijiji_Data"))
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
    ids=data['ad_id']
    data_to_append=pd.DataFrame(ids)
    excel_file_path = '{}_ids.xlsx'.format("Kijiji_Autos")

    try:
        existing_data = pd.read_excel(excel_file_path)

        combined_data = pd.concat([existing_data, data_to_append], ignore_index=True)

        
    except FileNotFoundError:
        combined_data = data_to_append
    try:
        combined_data.to_excel(excel_file_path, index=False)
    except:
        pass

def create_kiji_ids(self,data):
    ids=data['ad_id']
    data_to_append=pd.DataFrame(ids)
    excel_file_path = '{}_ids.xlsx'.format("Kijiji")

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
        if(type=="Kijiji_Autos"):
            xl = pd.ExcelFile('Kijiji_Autos_ids.xlsx')
        elif(type=="Kijiji"):
            xl = pd.ExcelFile('Kijiji_ids.xlsx')
        df = xl.parse('Sheet1')

        if id in df['ad_id'].values:
            return True
    except:
        return False
    return False
