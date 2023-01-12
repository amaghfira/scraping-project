from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

chrome_options = Options()
driver = webdriver.Chrome("D:\AMAGHFIRA\monit-auto-uploader\chromedriver.exe")
driver.get("https://search.prokal.co/?q=impor")
time.sleep(5)
# print(driver.title)

# search = driver.find_element("name","search")
# search.send_keys("impor")
# search.send_keys(Keys.RETURN)
# assert "No Result Found" not in driver.page_source


# scrap berita starts here
boxes = driver.find_elements(By.CSS_SELECTOR,value='#___gcse_0 > div > div > div > div.gsc-wrapper > div.gsc-resultsbox-visible > div > div > div.gsc-expansionArea > div > div.gs-webResult.gs-result > div.gsc-thumbnail-inside > div')
print(len(boxes))
for box in boxes :
    link = box.find_element(By.CSS_SELECTOR,value='#___gcse_0 > div > div > div > div.gsc-wrapper > div.gsc-resultsbox-visible > div > div > div.gsc-expansionArea > div > div.gs-webResult.gs-result > div.gsc-thumbnail-inside > div > a')
    print(link.text)
    link.click()
    driver.close()

time.sleep(2)


# close browser 
driver.quit()