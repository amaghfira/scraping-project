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

PATCH = 'D:\AMAGHFIRA\python-project\scrap_news\chromedriver120.exe'

def wait_element(driver, time, by, sel):
    # element = WebDriverWait(d, time).until(EC.presence_of_element_located((By.CSS_SELECTOR, sel)))
    element_present = EC.presence_of_element_located((by,sel))
    WebDriverWait(driver, time).until(element_present)

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')

driver = webdriver.Chrome(PATCH,options=options)
driver.get("https://st2023-query.bps.go.id/")
driver.maximize_window()
time.sleep(3)  

# LOGIN 
username = driver.find_element(By.CSS_SELECTOR, value='#username')
username.send_keys('aulia.maghfira')
password = driver.find_element(By.CSS_SELECTOR, value='#password')
password.send_keys('4uL14m49h')
password.send_keys(Keys.ENTER)

# CLICK LOAD 
click_load = driver.find_element(By.CSS_SELECTOR, value='#sidebar > div:nth-child(3) > button.btn.btn-warning.flex-fill.mr-1')
click_load.click()
driver.implicitly_wait(10)

# CLICK SERVER 
click_server = driver.find_element(By.CSS_SELECTOR, value='#server')
click_server.click()
driver.implicitly_wait(10) 

# CLICK LOAD ALL QUERY
load_query = driver.find_element(By.CSS_SELECTOR, value='#viewSavedQueriesModal > div > div > div.modal-body > table > thead > tr > th:nth-child(5) > button')
load_query.click()
driver.implicitly_wait(10)

load_query_yes = driver.find_element(By.CSS_SELECTOR, value='body > div.swal2-container.swal2-center.swal2-backdrop-show > div > div.swal2-actions > button.swal2-confirm.swal2-styled')
load_query_yes.click()
driver.implicitly_wait(10)

# CLOSE POP UP 
close_popup = driver.find_element(By.CSS_SELECTOR, value='#viewSavedQueriesModal > div > div > div.modal-header.bg-primary.text-white > div.d-flex.flex-row.align-items-center > button')
close_popup.click()
driver.implicitly_wait(10)

# -------------------------------------------
# HANDLE QUERY 
# -------------------------------------------
    
# BUKA SATU PERSATU LINK QUERY 1-103
for i in range(1,104):
    # # Temukan elemen yang mengandung scrollbar
    # scrollable_element = driver.find_element(By.CSS_SELECTOR, '#sidebar > ul')

    # # Gunakan JavaScript untuk menggulirkan scrollbar
    # driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", scrollable_element)
    
    wait_element(driver=driver, time=10, by=By.CSS_SELECTOR, sel='#sidebar > ul > li.c-sidebar-nav-item.c-sidebar-nav-dropdown.c-show > ul > li:nth-child('+str(i)+')')
    
    print('query ke-'+str(i))
    # CLICK NAMA QUERY
    query = driver.find_element(By.CSS_SELECTOR, value='#sidebar > ul > li.c-sidebar-nav-item.c-sidebar-nav-dropdown.c-show > ul > li:nth-child('+str(i)+') > div') 
    query.click()
    
    try:
        element_judul = driver.find_element(By.XPATH, '//*[@id="sidebar"]/ul/li[2]/ul/li[' + str(i) + ']/div')
        judul = element_judul.text
        print(judul)
        
        wait_element(driver=driver, time=10, by=By.CSS_SELECTOR, sel='body > div > div > main > div > div > div.c-wrapper > div > main > div > div.container-fluid > div > div > div:nth-child(3) > div > div.card-body.p-2 > div > div > div > div > div.ace_editor.ace-sqlserver > div.ace_scroller > div > div.ace_layer.ace_text-layer > div')
        
        ace_line_group = driver.find_elements(By.CSS_SELECTOR, 'body > div > div > main > div > div > div.c-wrapper > div > main > div > div.container-fluid > div > div > div:nth-child(3) > div > div.card-body.p-2 > div > div > div > div > div.ace_editor.ace-sqlserver > div.ace_scroller > div > div.ace_layer.ace_text-layer > div')
        
        # Inisialisasi teks yang akan diambil
        full_text = ''

        # for j in range(1,len(ace_line_group)):
        # Temukan elemen dengan class "ace_line"
        wait_element(driver=driver, time=10, by=By.CLASS_NAME, sel="ace_line")
        
        ace_line_elements = driver.find_elements(By.CLASS_NAME, "ace_line")

        for ace_line_element in ace_line_elements:
            full_text += ace_line_element.get_attribute("textContent") + "\n"    

        print(full_text)
        
        
        # CREATE CSV 
        List = [judul,full_text]
        with open('D:\AMAGHFIRA\python-project\scrap_news\query.csv', 'a') as f_object:
            # Pass this file object to csv.writer()
            # and get a writer object
            writer_object = writer(f_object)
        
            # Pass the list as an argument into
            # the writerow()
            writer_object.writerow(List)
        
            # Close the file object
            f_object.close()
    except NoSuchElementException:
        pass
 

driver.close()