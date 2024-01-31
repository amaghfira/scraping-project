from operator import index
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
import time
import pandas as pd
import mysql.connector
# import chromedriver_autoinstaller
from webdriver_manager.chrome import ChromeDriverManager

db = mysql.connector.connect(
    host= "localhost",
    user= "root",
    password= "",
    database="scrap_berita"
)

# PATH = 'D:\AMAGHFIRA\python-project\scrap_news\chromedriver110.exe'

def wait_element(d, time, sel):
    element = WebDriverWait(d, time).until(EC.presence_of_element_located((By.CSS_SELECTOR, sel)))

# Chrome driver 
chrome_version = '120.0.6099.225'
# Automatically download and install the compatible ChromeDriver
driver = webdriver.Chrome(ChromeDriverManager().install())
# chromedriver_autoinstaller.install(cwd=True, version=chrome_version)
service = Service()
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')

driver = webdriver.Chrome(service=service,options=options)

# Firefox driver 


driver.get("https://search.bisnis.com/")
time.sleep(3)  

# ARRAY OF KEYWORDS (change keywords here)
keywords = [
    "pdrb kaltim",
    "ekonomi kaltim",
    "pdrb kalimantan timur",
    "ekonomi kalimantan timur"
]

# FIND SEARCH COLUMN  
search = driver.find_element(By.CSS_SELECTOR, value='#search > input[type=text]')

time.sleep(4)

# LOOP THROUGH LIST OF KEYWORDS
for word in keywords :
    search.send_keys(word)
    search.send_keys(Keys.ENTER)
    print(word)
    
    # loop through page 1
    konten = driver.find_elements(By.CSS_SELECTOR, 'body > div.wrapper-details.no-kanal.main-inject > div > div > div.col-custom.left > ul > li')
    print('jumlah konten:' + str(len(konten)))
    berita=[]
    
    for i in range(1,len(konten)):
            # driver1 = webdriver.Chrome(PATH)
            link = driver.find_element(By.CSS_SELECTOR, value="body > div.wrapper-details.no-kanal.main-inject > div > div > div.col-custom.left > ul > li:nth-child("+str(i)+") > div.col-sm-4 > a").get_attribute('href')
            print(link)
            driver1 = webdriver.Chrome(PATH)
            driver1.get(link)
            
            try: 
                judul = driver1.find_element(By.CSS_SELECTOR, 'body > div.wrapper-details > div > div > div.col-custom.left > h1').text
                tanggal = driver1.find_element(By.CSS_SELECTOR, 'body > div.wrapper-details > div > div > div.col-custom.left > div.author > div > span').text
                isi = driver1.find_element(By.CSS_SELECTOR, 'body > div.wrapper-details > div > div > div.col-custom.left > div.description > div > div').text
                sumber = 'kaltimbisnis.com'
                
                
                # INSERT INTO DB 
                mycursor = db.cursor()
                query = "INSERT INTO berita_20230803(judul,tanggal,isi,sumber) VALUES (%s,%s,%s,%s)"
                val = (judul,tanggal,isi,sumber)
                mycursor.execute(query,val)
                db.commit()
                print(mycursor.rowcount, "record inserted.")
            
                driver1.close()
            except NoSuchElementException:
                pass
            
    # if there are more pages, click next page
    try:
        nextPageLink = driver.find_element(By.CSS_SELECTOR,'body > div.wrapper-details.no-kanal.main-inject > div > div > div.col-custom.left > div.pages__wrapper.mt-75 > ul > li:nth-child(4) > a').get_attribute('href')
        driver1 = webdriver.Chrome(PATH)
        driver1.get(nextPageLink)
        
        konten = driver.find_elements(By.CSS_SELECTOR, 'body > div.wrapper-details.no-kanal.main-inject > div > div > div.col-custom.left > ul > li')
        print('jumlah konten:' + str(len(konten)))
        berita=[]
        
        for i in range(1,len(konten)):
            link = driver.find_element(By.CSS_SELECTOR, value="body > div.wrapper-details.no-kanal.main-inject > div > div > div.col-custom.left > ul > li:nth-child("+str(i)+") > div.col-sm-4 > a").get_attribute('href')
            print(link)
            driver1 = webdriver.Chrome(PATH)
            driver1.get(link)
            
            try: 
                judul = driver1.find_element(By.CSS_SELECTOR, 'body > div.wrapper-details > div > div > div.col-custom.left > h1').text
                tanggal = driver1.find_element(By.CSS_SELECTOR, 'body > div.wrapper-details > div > div > div.col-custom.left > div.author > div > span').text
                isi = driver1.find_element(By.CSS_SELECTOR, 'body > div.wrapper-details > div > div > div.col-custom.left > div.description > div > div').text
                sumber = 'kaltimbisnis.com'
                
                
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
    except NoSuchElementException:
        pass
    driver.close()

print("Data berhasil disimpan KE DATABASE")
driver.close()