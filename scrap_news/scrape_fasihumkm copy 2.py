import csv
from operator import index
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd
from csv import writer
import gspread
from google.oauth2.service_account import Credentials

# Authenticate with Google Sheets API using your credentials JSON file
scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

credentials = Credentials.from_service_account_file(
    'C:\\Users\\DELL\\AppData\\gspread\\service_account.json',
    scopes=scopes
)

gc = gspread.authorize(credentials)

# Open your Google Sheet by its title or URL
spreadsheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/1eUp63h-IH59U1wtsrSG0y1Y00kK82s390MxZ9TmQkVc/edit?usp=sharing")
worksheet = spreadsheet.get_worksheet(0)  # Use the index of the worksheet you want to write to (0 for the first sheet)

PATCH = 'D:\AMAGHFIRA\python-project\scrap_news\chromedriver117.exe'

def wait_element(driver, time, by, sel):
    # element = WebDriverWait(d, time).until(EC.presence_of_element_located((By.CSS_SELECTOR, sel)))
    element_present = EC.presence_of_element_located((by,sel))
    WebDriverWait(driver, time).until(element_present)

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')

driver = webdriver.Chrome(PATCH,options=options)
driver.get("https://fasih-sm.bps.go.id/oauth_login.html")
driver.maximize_window()
time.sleep(3)  

# LOGIN 
click_sso = driver.find_element(By.CSS_SELECTOR,value='#login-in > a.login-button')
click_sso.click()
driver.implicitly_wait(10)

username = driver.find_element(By.CSS_SELECTOR, value='#username')
username.send_keys('aulia.maghfira')
password = driver.find_element(By.CSS_SELECTOR, value='#password')
password.send_keys('4uL14m49h')
password.send_keys(Keys.ENTER)

# pilih menu pencacahan umkm
wait_element(driver=driver, time=30, by=By.CSS_SELECTOR, sel='#Pencacahan > tbody > tr:nth-child(1) > td:nth-child(1) > a')
click_umkm = driver.find_element(By.CSS_SELECTOR, value='#Pencacahan > tbody > tr:nth-child(1) > td:nth-child(1) > a')
click_umkm.click()

# fungsi scraping
def scrape_data():
    scraped_data = []  # Create an empty list to store scraped data
    
    for i in range(1, len(jml_item) + 1):
        try:
            print(str(i))
            kode_identitas = driver.find_element(by=By.XPATH, value=f'//*[@id="assignmentDatatable"]/tbody[2]/tr[{i}]/td[2]/a')
            nama_kk = driver.find_element(by=By.XPATH, value=f'//*[@id="assignmentDatatable"]/tbody[2]/tr[{i}]/td[3]')
            alamat = driver.find_element(by=By.XPATH, value=f'//*[@id="assignmentDatatable"]/tbody[2]/tr[{i}]/td[4]')
            no_keluarga = driver.find_element(by=By.XPATH, value=f'//*[@id="assignmentDatatable"]/tbody[2]/tr[{i}]/td[5]')
            no_bangunan = driver.find_element(by=By.XPATH, value=f'//*[@id="assignmentDatatable"]/tbody[2]/tr[{i}]/td[6]')
            jml_usaha = driver.find_element(by=By.XPATH, value=f'//*[@id="assignmentDatatable"]/tbody[2]/tr[{i}]/td[7]')
            status = driver.find_element(by=By.XPATH, value=f'//*[@id="assignmentDatatable"]/tbody[2]/tr[{i}]/td[8]')
            user = driver.find_element(by=By.XPATH, value=f'//*[@id="assignmentDatatable"]/tbody[2]/tr[{i}]/td[9]')
            
            
            # Append the scraped data to the list
            scraped_data.append({
                'kode_identitas': kode_identitas.text,
                'nama_kk': nama_kk.text,
                'alamat': alamat.text,
                'no_keluarga': no_keluarga.text,
                'no_bangunan': no_bangunan.text,
                'jml_usaha': jml_usaha.text,
                'status': status.text,
                'user': user.text
            })
        except NoSuchElementException:
            pass
        
    # Write the scraped data to a CSV file
    # with open('D:\\AMAGHFIRA\\python-project\\scrap_news\\umkm.csv', 'a', newline='', encoding='utf-8') as f_object:
    #     writer_object = csv.writer(f_object)
    #     writer_object.writerows(scraped_data)
    
    # Write the scraped data to the Google Sheet
    # worksheet.insert_rows(scraped_data, 2)

     # Retrieve existing data from the Google Sheet
    existing_data = worksheet.get_all_records()
    
    # Update the existing data based on matching kode_identitas
    for scraped_row in scraped_data:
        print('scraped row: '+scraped_row)
        for row in existing_data:
            if row['kode_identitas'] == scraped_row['kode_identitas']:
                # Update the row with the new data
                row.update({
                    'nama_kk': scraped_row['nama_kk'],
                    'alamat' : scraped_row['alamat'],
                    'no_keluarga' : scraped_row['no_keluarga'],
                    'no_bangunan' : scraped_row['no_bangunan'],
                    'jml_usaha' : scraped_row['jml_usaha'],
                    'status' : scraped_row['status'],
                    'user' : scraped_row['user']
                })
                break 
            else :
                worksheet.insert_rows([list(scraped_row.values())], 2) # Inserts the new data into the second row, adjust as needed
                
    # Write the updated data back to the Google Sheet
    worksheet.update([existing_data])
    
# Scrape data from the first page
wait_element(driver=driver, time=10, by=By.CSS_SELECTOR, sel='#assignmentDatatable')
jml_item = driver.find_elements(By.XPATH, value='//*[@id="assignmentDatatable"]/tbody[2]/tr')
print('jumlah item: '+str(len(jml_item)))
scrape_data()

# loop through pages
while True:
    try:
        # Locate the "next" button
        next_button = driver.find_element(by=By.XPATH, value='//*[@id="assignmentDatatable_next"]')
        
        if next_button.is_displayed():
            # If the "next" button is displayed, click it to go to the next page
            print("Going to the next page...")
            next_button.click()
            
            # Wait for the new page to load
            time.sleep(5)  # Adjust the sleep time as needed

            # Re-fetch elements for the new page
            wait_element(driver=driver, time=10, by=By.CSS_SELECTOR, sel='#assignmentDatatable')
            jml_item = driver.find_elements(By.XPATH, value='//*[@id="assignmentDatatable"]/tbody[2]/tr')
            print('jumlah item: '+str(len(jml_item)))

            # Scrape data on the new page
            scrape_data()
        else:
            # If the "next" button is not displayed, exit the loop
            print("No next button found. Exiting.")
            break

    except NoSuchElementException:
        # If the "next" button is not found, exit the loop
        print("No next button found. Exiting.")
        break

# ... Rest of your code ...

driver.close()
