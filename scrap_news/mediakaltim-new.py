from operator import index
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import time
import pandas as pd
import mysql.connector

db = mysql.connector.connect(
    host= "localhost",
    user= "root",
    password= "",
    database="scrap_berita"
)

path = 'D:\AMAGHFIRA\python-project\scrap_news\chromedriver-120.exe'

def wait_element(d, time, sel):
    element = WebDriverWait(d, time).until(EC.presence_of_element_located((By.CSS_SELECTOR, sel)))

def getNewsDetails() :
    # GET NEWS FROM 1st PAGE
        news = driver.find_elements(By.CSS_SELECTOR, value='#tdi_65 > div')
        print('jumlah konten:' + str(len(news)))
        berita=[]
        
        # GET CONTENTS OF EACH NEWS 
        for i in range(1,len(news)):
            
            link = driver2.find_element(By.CSS_SELECTOR, value="#tdi_65 > div:nth-child("+str(i)+") > div > div.td-module-meta-info > h3 > a").get_attribute('href')
            print(link)
            
            driver1 = webdriver.Chrome(path)
            driver1.get(link)
            
            try: 
                judul = driver1.find_element(By.CSS_SELECTOR, '#tdi_58 > div > div.vc_column.tdi_61.wpb_column.vc_column_container.tdc-column.td-pb-span8 > div > div.td_block_wrap.tdb_title.tdi_63.tdb-single-title.td-pb-border-top.td_block_template_1 > div > h1').text
                print(judul)
                tanggal = driver1.find_element(By.CSS_SELECTOR, '#tdi_58 > div > div.vc_column.tdi_61.wpb_column.vc_column_container.tdc-column.td-pb-span8 > div > div.td_block_wrap.tdb_single_date.tdi_65.td-pb-border-top.td_block_template_1.tdb-post-meta > div > time').text
                print(tanggal)
                isi = driver1.find_element(By.CSS_SELECTOR, '#tdi_58 > div > div.vc_column.tdi_61.wpb_column.vc_column_container.tdc-column.td-pb-span8 > div > div.td_block_wrap.tdb_single_content.tdi_69.td-pb-border-top.td_block_template_1.td-post-content.tagdiv-type > div').text
                print(isi)
                sumber = 'mediakaltim.com'
                
                
                # INSERT INTO DB 
                mycursor = db.cursor()
                query = "INSERT INTO berita_20240122(judul,tanggal,isi,sumber) VALUES (%s,%s,%s,%s)"
                val = (judul,tanggal,isi,sumber)
                mycursor.execute(query,val)
                db.commit()
                print(mycursor.rowcount, "record inserted.")
            
                driver1.close()
            except NoSuchElementException:
                pass
# USING CHROME  
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')

driver = webdriver.Chrome(path,chrome_options=options)

# USING FIREFox
# options = FirefoxOptions()
# options.add_argument("--headless")
# driver = webdriver.Firefox()

# OPEN WEBSITE
driver.get("https://mediakaltim.com/?s")
time.sleep(3)  

# ARRAY OF KEYWORDS (change keywords here)
keywords = [
    # "belanja online",
    # "toko online",
    # "shopee",
    # "lazada",
    # "tokopedia",
    "marketplace"
]

# FIND SEARCH COLUMN  
search = driver.find_element(By.CSS_SELECTOR, value='#tdb-search-form-input-tdi_64')

time.sleep(4)

# LOOP THROUGH LIST OF KEYWORDS
for word in keywords :
    search.send_keys(word)
    search.send_keys(Keys.ENTER)
    print(word)
    
    try :
        numPages = driver.find_elements(By.CSS_SELECTOR, value='#tdi_59 > div > div.vc_column.tdi_62.wpb_column.vc_column_container.tdc-column.td-pb-span8 > div > div.td_block_wrap.tdb_loop.tdi_65.tdb-numbered-pagination.td_with_ajax_pagination.td-pb-border-top.td_block_template_1.tdb-category-loop-posts > div.page-nav.td-pb-padding-side > a')
        
        # HALAMAN PERTAMA 
        # getNewsDetails()
        # NEXT PAGE 
        if (len(numPages) <= 3) :
            for i in range(1,len(numPages)) :
                print("halaman ke - "+str(i))
                linkToNextPage = "https://mediakaltim.com/page/"+str(i)+"/?s="+word
                print(linkToNextPage)
                driver2 = webdriver.Chrome(path)
                driver2.get(linkToNextPage)
                getNewsDetails()
        if len(numPages) > 3:
            for i in range(1,3) :
                print("halaman ke - "+str(i))
                linkToNextPage = "https://mediakaltim.com/page/"+str(i)+"/?s="+word
                print(linkToNextPage)
                driver2 = webdriver.Chrome(path)
                driver2.get(linkToNextPage)
                getNewsDetails()
                
    except NoSuchElementException:
        pass
    
print("Data berhasil disimpan KE DATABASE")
driver2.close()
driver.close()