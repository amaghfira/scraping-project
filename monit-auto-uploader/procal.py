from operator import index
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

PATH = 'D:\AMAGHFIRA\monit-auto-uploader\chromedriver.exe'

def wait_element(d, time, sel):
    element = WebDriverWait(d, time).until(EC.presence_of_element_located((By.CSS_SELECTOR, sel)))

driver = webdriver.Chrome(PATH)
driver.get("https://search.prokal.co/?q=impor")
time.sleep(3)  
#div.content-artikel-judul
halaman = driver.find_elements(By.CSS_SELECTOR, value='#___gcse_0 > div > div > div > div.gsc-wrapper > div.gsc-resultsbox-visible > div > div > div.gsc-expansionArea > div > div.gs-webResult.gs-result > div.gsc-thumbnail-inside > div')


print(len(halaman))
berita=[]
for data in halaman:
    link = data.find_element(By.CSS_SELECTOR, "#___gcse_0 > div > div > div > div.gsc-wrapper > div.gsc-resultsbox-visible > div > div > div.gsc-expansionArea > div > div.gs-webResult.gs-result > div.gsc-thumbnail-inside > div > a")
    newpath = link.get_attribute('href')
    driver1 = webdriver.Chrome(PATH)
    link.click()
    driver1.get(newpath)
    judul = driver1.find_element(By.CSS_SELECTOR, 'div.content-artikel-judul').text
    tanggal = driver1.find_element(By.CSS_SELECTOR, 'div.content-artikel > small').text
    isi = driver1.find_element(By.CSS_SELECTOR, '#bodytext').text
    dt_berita = {
                'judul' : judul,
                'tanggal' : tanggal,
                'isi' : isi
                }
    berita.append(dt_berita)
    driver1.close()

df = pd.DataFrame(berita)
df.to_excel('Procal.xlsx',index=False)
print("Data berhasil disimpan dalam bentuk excel")
driver.close()