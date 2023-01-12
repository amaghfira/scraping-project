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
import mysql.connector

db = mysql.connector.connect(
    host= "localhost",
    user= "root",
    password= "",
    database="scrap_berita"
)

PATCH = 'D:\AMAGHFIRA\python-project\scrap_news\chromedriver108.exe'

def wait_element(d, time, sel):
    element = WebDriverWait(d, time).until(EC.presence_of_element_located((By.CSS_SELECTOR, sel)))

driver = webdriver.Chrome(PATCH)
driver.get("https://search.prokal.co/")
time.sleep(3)  

# array keyword
keywords = [
    "ekspor malaysia",
    "ekspor filipina",
    "ekspor philippine",
    "ekspor thailand"
]

search = driver.find_element(By.NAME, value='search')

# sort by date 
# bydate = driver.find_element(By.CSS_SELECTOR, value='#___gcse_0 > div > div > div > div.gsc-above-wrapper-area > table > tbody > tr > td.gsc-orderby-container > div > div.gsc-option-menu-container.gsc-inline-block > div.gsc-option-menu')
# bydate.send_keys(Keys.ENTER)
# dates = driver.find_element(By.CSS_SELECTOR, value='#___gcse_0 > div > div > div > div.gsc-above-wrapper-area > table > tbody > tr > td.gsc-orderby-container > div > div.gsc-option-menu-container.gsc-inline-block > div.gsc-option-menu-invisible > div.gsc-option-menu-item.gsc-option-menu-item-highlighted')
# dates.send_keys(Keys.ENTER)
# filter_button = Select(driver.find_element(By.XPATH, value='//*[@id="___gcse_0"]/div/div/div/div[3]/table/tbody/tr/td[2]/div/div[2]'))
# filter_button.click()
time.sleep(5)
for word in keywords :
    search.send_keys(word)
    search.send_keys(Keys.ENTER)
    print(word)
    pages = driver.find_elements(By.CSS_SELECTOR, value='#___gcse_0 > div > div > div > div.gsc-wrapper > div.gsc-resultsbox-visible > div > div > div.gsc-cursor-box.gs-bidi-start-align > div >div')
    print(len(pages))
    for i in range(2,len(pages)-4):
        print(i)
        j = str(i)
        page = driver.find_element(By.CSS_SELECTOR, value='#___gcse_0 > div > div > div > div.gsc-wrapper > div.gsc-resultsbox-visible > div > div > div.gsc-cursor-box.gs-bidi-start-align > div >div:nth-child('+j+')') 
        page.send_keys(Keys.RETURN)
        time.sleep(3)
        halaman = driver.find_elements(By.CSS_SELECTOR, value='#___gcse_0 > div > div > div > div.gsc-wrapper > div.gsc-resultsbox-visible > div > div > div.gsc-expansionArea > div > div.gs-webResult.gs-result > div.gsc-thumbnail-inside > div')
        print(len(halaman))
        berita=[]
        for data in halaman:
            link = data.find_element(By.CSS_SELECTOR, "#___gcse_0 > div > div > div > div.gsc-wrapper > div.gsc-resultsbox-visible > div > div > div.gsc-expansionArea > div > div.gs-webResult.gs-result > div.gsc-thumbnail-inside > div > a").get_attribute('href')
            driver1 = webdriver.Chrome(PATCH)
            driver1.get(link)
            try: 
                judul = driver1.find_element(By.CSS_SELECTOR, 'div.content-artikel-judul').text
                tanggal = driver1.find_element(By.CSS_SELECTOR, 'div.content-artikel > small').text
                isi = driver1.find_element(By.CSS_SELECTOR, '#bodytext').text
                dt_berita = {
                            'judul' : judul,
                            'tanggal' : tanggal,
                            'isi' : isi
                            }
                berita.append(dt_berita)
                
                # insert into db 
            #     mycursor = db.cursor()
            #     query = "INSERT INTO berita_20230111(judul,tanggal,isi) VALUES (%s,%s,%s)"
            #     val = (judul,tanggal,isi)
            #     mycursor.execute(query,val)
            #     db.commit()
            #     print(mycursor.rowcount, "record inserted.")
                
                driver1.close()
            except NoSuchElementException:
                pass
df = pd.DataFrame(berita)
df.to_excel('Procalnew20230111.xlsx',index=False)
print("Data berhasil disimpan dalam bentuk excel")
driver.close()