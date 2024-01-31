import csv
from operator import index
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
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

# Open Google Sheet by URL
spreadsheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/1eUp63h-IH59U1wtsrSG0y1Y00kK82s390MxZ9TmQkVc/edit?usp=sharing")
worksheet = spreadsheet.get_worksheet(0)  # Use the index of the worksheet you want to write to (0 for the first sheet)

PATCH = 'D:\AMAGHFIRA\python-project\scrap_news\chromedriver120.exe'

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
password.send_keys('*********') # edit here
password.send_keys(Keys.ENTER)

# choose menu pencacahan umkm
wait_element(driver=driver, time=30, by=By.CSS_SELECTOR, sel='#Pencacahan > tbody > tr:nth-child(1) > td:nth-child(1) > a')
click_umkm = driver.find_element(By.CSS_SELECTOR, value='#Pencacahan > tbody > tr:nth-child(1) > td:nth-child(1) > a')
click_umkm.click()

# ############### #
# FUNGSI SCRAPING #
# ############### #

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
        except StaleElementReferenceException:
            print("Stale element detected. Retrying...")
            continue  # Skip this iteration and try again
   
     # Retrieve existing data from the Google Sheet
    existing_data = worksheet.get_all_records()
    kode_identitas_list = worksheet.col_values(1)

    # Prepare a list for new data that will be inserted
    new_data = []

    # Update the existing data based on matching kode_identitas
    for scraped_row in scraped_data:
        kode_identitas = scraped_row['kode_identitas']

        if kode_identitas in kode_identitas_list:
            index = kode_identitas_list.index(kode_identitas)
            # Check if the index is valid
            if 0 <= index < len(existing_data):
                existing_data[index].update({
                    'nama_kk': scraped_row['nama_kk'],
                    'alamat': scraped_row['alamat'],
                    'no_keluarga': scraped_row['no_keluarga'],
                    'no_bangunan': scraped_row['no_bangunan'],
                    'jml_usaha': scraped_row['jml_usaha'],
                    'status': scraped_row['status'],
                    'user': scraped_row['user']
                })
            else: 
                print(f"Warning: Invalid index for kode_identitas '{kode_identitas}'")
        else:
            # If 'kode_identitas' is not in the existing data, insert it
            new_data.append([
                scraped_row['kode_identitas'],
                scraped_row['nama_kk'],
                scraped_row['alamat'],
                scraped_row['no_keluarga'],
                scraped_row['no_bangunan'],
                scraped_row['jml_usaha'],
                scraped_row['status'],
                scraped_row['user']
            ])

    # # Check if the Google Sheet is empty
    # uncomment this code if the spreadsheet is still blank
    # if not existing_data:
    #     # Insert the header row with column names
    #     header_row = [
    #         'kode_identitas',
    #         'nama_kk',
    #         'alamat',
    #         'no_keluarga',
    #         'no_bangunan',
    #         'jml_usaha',
    #         'status',
    #         'user'
    #     ]
    #     worksheet.insert_rows([header_row], 1)

    # Insert new data into the Google Sheet
    if new_data:
        # Inserts the new data into the second row, adjust as needed
        worksheet.insert_rows(new_data, 2)

    # ... Continue with your code ...


# show 100 data 
select = driver.find_element(by=By.XPATH, value='//*[@id="assignmentDatatable_length"]/label/select')
select.click()
wait_element(driver=driver, time=5, by=By.XPATH, sel='//*[@id="assignmentDatatable_length"]/label/select/option[4]')
select100 = driver.find_element(by=By.XPATH, value='//*[@id="assignmentDatatable_length"]/label/select/option[4]')
select100.click()

# ###########
# FILTERING #
# ###########
wait_element(driver=driver, time=10, by=By.CSS_SELECTOR, sel='body > app-root > horizontal-layout > div.app-content.content > content > div > app-collectsurvey > div > div.sidebar-opener.col-sm-12.ng-star-inserted > button')
# filter_button = driver.find_element(by=By.CSS_SELECTOR, value='body > app-root > horizontal-layout > div.app-content.content > content > div > app-collectsurvey > div > div.sidebar-opener.col-sm-12.ng-star-inserted > button')
filter_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > app-root > horizontal-layout > div.app-content.content > content > div > app-collectsurvey > div > div.sidebar-opener.col-sm-12.ng-star-inserted > button'))
)
filter_button.click()
print("filter button clicked!")

wait_element(driver=driver, time=10, by=By.XPATH, sel='/html/body/app-root/horizontal-layout/div[2]/content/div/app-collectsurvey/div/div[3]/div[2]/div/div/div[1]/div/div/ngx-select/div')
filter_prov = driver.find_element(by=By.XPATH, value='/html/body/app-root/horizontal-layout/div[2]/content/div/app-collectsurvey/div/div[3]/div[2]/div/div/div[1]/div/div/ngx-select/div')
filter_prov.click()
print("filter prov clicked!")

wait_element(driver=driver, time=10, by=By.XPATH, sel='/html/body/app-root/horizontal-layout/div[2]/content/div/app-collectsurvey/div/div[3]/div[2]/div/div/div[1]/div/div/ngx-select/div/ngx-select-choices/ul/li/a')
kaltim = driver.find_element(by=By.XPATH, value='/html/body/app-root/horizontal-layout/div[2]/content/div/app-collectsurvey/div/div[3]/div[2]/div/div/div[1]/div/div/ngx-select/div/ngx-select-choices/ul/li/a')
element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/horizontal-layout/div[2]/content/div/app-collectsurvey/div/div[3]/div[2]/div/div/div[1]/div/div/ngx-select/div/ngx-select-choices/ul/li/a')))
element.click()
print("kaltim clicked!")

wait_element(driver=driver, time=10, by=By.XPATH, sel='/html/body/app-root/horizontal-layout/div[2]/content/div/app-collectsurvey/div/div[3]/div[2]/div/div/div[2]/div/div/ngx-select/div')

filter_kab = driver.find_element(by=By.XPATH, value='/html/body/app-root/horizontal-layout/div[2]/content/div/app-collectsurvey/div/div[3]/div[2]/div/div/div[2]/div/div/ngx-select/div').click()
for i in range(1,4) :
    nama_kab = driver.find_element(by=By.XPATH, value='/html/body/app-root/horizontal-layout/div[2]/content/div/app-collectsurvey/div/div[3]/div[2]/div/div/div[2]/div/div/ngx-select/div/ngx-select-choices/ul/li['+str(i)+']/a').click()
    
    wait_element(driver=driver, time=10, by=By.XPATH, sel='/html/body/app-root/horizontal-layout/div[2]/content/div/app-collectsurvey/div/div[3]/div[2]/div/div/div[3]/div/div/ngx-select/div')
    
    filter_kec = driver.find_element(by=By.XPATH, value='/html/body/app-root/horizontal-layout/div[2]/content/div/app-collectsurvey/div/div[3]/div[2]/div/div/div[3]/div/div/ngx-select/div').click()
    nama_kec_list = driver.find_elements(by=By.XPATH, value='//*[@id="region3Id"]/div/ngx-select-choices/ul/li')
    print(len(nama_kec_list))
    for j in range(1,len(nama_kec_list)+1) :
        filter_kec = driver.find_element(by=By.XPATH, value='/html/body/app-root/horizontal-layout/div[2]/content/div/app-collectsurvey/div/div[3]/div[2]/div/div/div[3]/div/div/ngx-select/div').click()
        nama_kec = driver.find_element(by=By.CSS_SELECTOR, value='#region3Id > div > ngx-select-choices > ul > li:nth-child('+str(j)+')').click()

        wait_element(driver=driver, time=10, by=By.CSS_SELECTOR, sel='#region4Id > div')
        
        filter_desa = driver.find_element(by=By.CSS_SELECTOR, value='#region4Id > div').click()
        nama_desa_list = driver.find_elements(by=By.XPATH, value='//*[@id="region4Id"]/div/ngx-select-choices/ul/li')
        for k in range(1,len(nama_desa_list)) :
            print(nama_desa_list)
            filter_desa = driver.find_element(by=By.CSS_SELECTOR, value='#region4Id > div').click()
            nama_desa = driver.find_element(by=By.XPATH, value='//*[@id="region4Id"]/div/ngx-select-choices/ul/li['+str(k)+']/a').click()
            
            filter_button2 = driver.find_element(by=By.CSS_SELECTOR, value='body > app-root > horizontal-layout > div.app-content.content > content > div > app-collectsurvey > div > div.sidebar-slider.sidebar-slide-in > div.sidebar-content > div > button:nth-child(3)').click()

            filter_button.click()
            
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
                    
                    # Check if the "disabled" attribute is present and set to "true"
                    # If the "next" button is clickable, click it to go to the next page
                    if next_button.is_displayed() and next_button.get_attribute("disabled") == "false":
                        
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

driver.close()
