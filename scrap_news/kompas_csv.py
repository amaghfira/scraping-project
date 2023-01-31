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

PATCH = 'D:\AMAGHFIRA\python-project\scrap_news\chromedriver108.exe'

def wait_element(d, time, sel):
    element = WebDriverWait(d, time).until(EC.presence_of_element_located((By.CSS_SELECTOR, sel)))

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')

driver = webdriver.Chrome(PATCH,chrome_options=options)
driver.get("https://kompas.com")
time.sleep(3)  

# ARRAY OF KEYWORDS 
keywords = [
    "ekspor kaltim"
]

# FIND SEARCH COLUMN  
search = driver.find_element(By.CSS_SELECTOR, value='#search')

time.sleep(4)

# LOOP THROUGH LIST OF KEYWORDS
for word in keywords :
    search.send_keys(word)
    search.send_keys(Keys.ENTER)
    print(word)
    
    # FIND NUMBER OF PAGES FOUND
    pages = driver.find_elements(By.CSS_SELECTOR, value='#___gcse_0 > div > div > div > div.gsc-wrapper > div.gsc-resultsbox-visible > div > div > div.gsc-cursor-box.gs-bidi-start-align > div > div.gsc-cursor-page')
    print('jumlah halaman: '+str(len(pages)))
    
    # LOOP THROUGH PAGES 
    for i in range(2,len(pages)):
        j = str(i)
        print('halaman ke- '+j)
        # ENTER EACH PAGE 
        page = driver.find_element(By.CSS_SELECTOR, value='#___gcse_0 > div > div > div > div.gsc-wrapper > div.gsc-resultsbox-visible > div > div > div.gsc-cursor-box.gs-bidi-start-align > div > div:nth-child('+j+')') 
        page.send_keys(Keys.ENTER)
        time.sleep(3)
        
        # LOOP THROUGH EACH PAGE TO FIND CONTENTS 
        halamans = driver.find_elements(By.CSS_SELECTOR, value='#___gcse_0 > div > div > div > div.gsc-wrapper > div.gsc-resultsbox-visible > div > div > div.gsc-expansionArea > div')
        print('jumlah konten:' + str(len(halamans)))
        berita=[]
        
        # GET CONTENTS 
        for i in range(4,len(halamans)):
            link = driver.find_element(By.CSS_SELECTOR, value="#___gcse_0 > div > div > div > div.gsc-wrapper > div.gsc-resultsbox-visible > div > div > div.gsc-expansionArea > div:nth-child("+str(i)+") > div.gs-webResult.gs-result > div.gsc-thumbnail-inside > div > a").get_attribute('href')
            print(link)
            driver1 = webdriver.Chrome(PATCH)
            driver1.get(link)
            
            try: 
                judul = driver1.find_element(By.CSS_SELECTOR, 'body > div.wrap > div.container.clearfix > div:nth-child(3) > div > h1').text
                tanggal = driver1.find_element(By.CSS_SELECTOR, 'body > div.wrap > div.container.clearfix > div.row.col-offset-fluid.clearfix.js-giant-wp-sticky-parent > div.col-bs10-7.js-read-article > div.read__header.col-offset-fluid.clearfix > div:nth-child(1) > div').text
                isi = driver1.find_element(By.CSS_SELECTOR, 'body > div.wrap > div.container.clearfix > div.row.col-offset-fluid.clearfix.js-giant-wp-sticky-parent > div.col-bs10-7.js-read-article > div.read__article.mt2.clearfix.js-tower-sticky-parent > div.col-bs9-7 > div.read__content > div').text
                sumber = 'kompas.com'
                
                List = [judul,tanggal,isi,sumber]
                with open('D:\AMAGHFIRA\python-project\scrap_news\datanew.csv', 'a') as f_object:
                    # Pass this file object to csv.writer()
                    # and get a writer object
                    writer_object = writer(f_object)
                
                    # Pass the list as an argument into
                    # the writerow()
                    writer_object.writerow(List)
                
                    # Close the file object
                    f_object.close()
                driver1.close()
            except NoSuchElementException:
                pass

driver.close()