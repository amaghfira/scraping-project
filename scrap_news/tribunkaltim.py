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

def wait_element(d, time, by, sel):
    element = WebDriverWait(d, time).until(EC.presence_of_element_located((by, sel)))

def getNewsDetails(keyword, driver) :
        word = keyword
        news = driver.find_elements(By.CSS_SELECTOR, value='#___gcse_0 > div > div > div > div.gsc-wrapper > div.gsc-resultsbox-visible > div > div > div.gsc-expansionArea > div')
        print('jumlah konten:' + str(len(news)))
        
        # GET CONTENTS OF EACH NEWS 
        for i in range(1,len(news)):
            
            link = driver.find_element(By.CSS_SELECTOR, value="#___gcse_0 > div > div > div > div.gsc-wrapper > div.gsc-resultsbox-visible > div > div > div.gsc-expansionArea > div:nth-child("+str(i)+") > div > div.gsc-thumbnail-inside > div > a").get_attribute('href')
            print(link)
            
            driver1 = webdriver.Chrome(path)
            driver1.get(link)
            
            try: 
                judul = driver1.find_element(By.CSS_SELECTOR, '#arttitle').text
                print(judul)
                tanggal = driver1.find_element(By.CSS_SELECTOR, '#article > div.grey.bdr3.pb10.pt10 > time').text
                print(tanggal)
                isi_text = driver1.find_element(By.XPATH, '/html/body/div[5]/div[6]/div[1]/div[1]/div').text
                # isi = []
                # paragraf = driver1.find_elements(By.XPATH, '/html/body/div[5]/div[6]/div[1]/div[1]/div/div[3]/div[5]/p')
                
                # wait_element(d=driver1, time=5, by=By.XPATH, sel='/html/body/div[5]/div[6]/div[1]/div[1]/div/div[3]/div[5]/p')
                
                # for j in range(1,len(paragraf)+1):
                #     kalimat = driver1.find_element(By.XPATH, '/html/body/div[5]/div[6]/div[1]/div[1]/div/div[3]/div[5]/p['+str(j)+']').text
                #     isi.append(kalimat)
                #     print("isi: "+isi)
                    
                # # Join isi into a single string with newline character
                # isi_text = "\n".join(isi)
                print("isi:", isi_text)
                sumber = 'tribunkaltim'
                
                # INSERT INTO DB 
                mycursor = db.cursor()
                query = "INSERT INTO berita_20240125(judul,tanggal,isi,sumber,keyword) VALUES (%s,%s,%s,%s,%s)"
                val = (judul,tanggal,isi_text,sumber,word)
                mycursor.execute(query,val)
                db.commit()
                print(mycursor.rowcount, "record inserted.")
            
                driver1.close()
            except Exception as e:
                print(f"Error processing news: {e}")
                with open('error_log.txt', 'a') as f:
                    f.write(f"Error processing news - {word}: {e}\n")
                pass
            
# USING CHROME  
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_argument('--headless')

# USING FIREFox
# options = FirefoxOptions()
# options.add_argument("--headless")
# driver = webdriver.Firefox()

# ARRAY OF KEYWORDS (change keywords here)
keywords = [
    "harga makanan jadi samarinda",
    "harga makanan jadi penajam paser utara"
]

time.sleep(4)
# ---------------------------------------------------------------------
# LOOP THROUGH LIST OF KEYWORDS
for word in keywords :
    # OPEN WEBSITE
    driver = webdriver.Chrome(path,chrome_options=options)
    driver.get("https://kaltim.tribunnews.com/search?q="+word)
    time.sleep(3)  
    print(word)
    
    try :
        # ambil dari halaman 1 
        print('halaman-1')
        getNewsDetails(keyword=word, driver=driver)
        numPages = driver.find_elements(By.CSS_SELECTOR, value='#___gcse_0 > div > div > div > div.gsc-wrapper > div.gsc-resultsbox-visible > div > div > div.gsc-cursor-box.gs-bidi-start-align > div > div')
        
        for k in range(2,len(numPages)) :
            print("halaman ke - "+str(k))
            linkToNextPage = "https://kaltim.tribunnews.com/search#gsc.tab=0&gsc.q="+word+"&gsc.sort=&gsc.page="+str(k)
            print(linkToNextPage)
            driver2 = webdriver.Chrome(path)
            driver2.get(linkToNextPage)
            getNewsDetails(keyword=word, driver=driver2)
            driver2.close()
            
        print("Data berhasil disimpan KE DATABASE")
        driver.close()
    except NoSuchElementException:
        pass
    
    
