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

wait_element(driver=driver, time=10, by=By.CSS_SELECTOR, sel='#assignmentDatatable')
jml_item = driver.find_elements(By.XPATH, value='//*[@id="assignmentDatatable"]/tbody[2]/tr')
print('jumlah item: '+str(len(jml_item)))


while True:
    # Loop through the data on the current page
    for i in range(1, len(jml_item) + 1):
        try:
            print(str(i))
            kode_identitas = driver.find_element(by=By.XPATH, value='//*[@id="assignmentDatatable"]/tbody[2]/tr[' + str(i) + ']/td[2]/a')
            nama_kk = driver.find_element(by=By.XPATH, value='//*[@id="assignmentDatatable"]/tbody[2]/tr[' + str(i) + ']/td[3]')
            print(kode_identitas.text)
            print(nama_kk.text)
        except NoSuchElementException:
            pass

    try:
        # Check if the "next" button exists
        next_button = driver.find_element(by=By.XPATH, value='//*[@id="assignmentDatatable_next"]')
        
        if next_button.is_displayed():
            next_button.click()
            print("next button exists.")
            
            time.sleep(10)
            
            
            wait_element(driver=driver, time=10, by=By.CSS_SELECTOR, sel='#assignmentDatatable')
            jml_item = driver.find_elements(By.XPATH, value='//*[@id="assignmentDatatable"]/tbody[2]/tr')
            print('jumlah item: '+str(len(jml_item)))
            for i in range(1,len(jml_item)+1):
                try:
                    print(str(i))
                    wait_element(driver=driver, time=10, by=By.XPATH, sel='//*[@id="assignmentDatatable"]/tbody[2]/tr['+str(i)+']/td[2]/a')
                    kode_identitas = driver.find_element(by=By.XPATH, value='//*[@id="assignmentDatatable"]/tbody[2]/tr['+str(i)+']/td[2]/a')
                    wait_element(driver=driver, time=10, by=By.XPATH, sel='//*[@id="assignmentDatatable"]/tbody[2]/tr['+str(i)+']/td[3]')
                    nama_kk = driver.find_element(by=By.XPATH, value='//*[@id="assignmentDatatable"]/tbody[2]/tr['+str(i)+']/td[3]')
                    
                    print(kode_identitas.text)
                    print(nama_kk.text)
                    
                except NoSuchElementException:
                    pass    
        else:
            # If the "next" button is not displayed, exit the loop
            print("No next button found. Exiting.")
            break

    except NoSuchElementException:
        # If the "next" button is not found, exit the loop
        print("No next button found. Exiting.")
        break


driver.close()