from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC  
from bs4 import BeautifulSoup
import openpyxl, time, datetime


now = datetime.datetime.now()
SSO_REFERRER = "https://sso.bps.go.id/auth/realms/pegawai-bps/protocol/openid-connect/auth?state=15c569fc98ebd65a8f8701f029ca516c&scope=name%2Cemail&response_type=code&approval_prompt=auto&redirect_uri=https%3A%2F%2Fregsosek-location.cloud.bps.go.id%2Fpublic%2Fsso%2Fbps&client_id=03140-wilkerstat-89w"

# ------- Fungsi Fungsi --------- #
# tidak jadi dipakai
def login_credentials(driver, sso_site, username, pwd) :
    driver.get(sso_site)
    driver.find_element(By.CSS_SELECTOR, "#username").send_keys(username)
    driver.find_element(By.CSS_SELECTOR, "#password").send_keys(pwd)
    driver.find_element(By.CSS_SELECTOR, "#kc-login").click()

# ------------------------------- #
    
chrome_options = Options()
# chrome_options.add_argument("--start-maximized")
#chrome_options.add_argument("--headless") #turn on kalo mau headless

# load driver 
driver = webdriver.Chrome("D:\AMAGHFIRA\python-project\scrapregsosek\chromedriver.exe") #path_to_your_chromedriver_or_gecko

# masuk ke web regsosek wilkerstat
driver.get("https://regsosek-location.cloud.bps.go.id/public/login")
driver.maximize_window()

# buka login ssso
driver.find_element(By.CSS_SELECTOR, "body > div > div:nth-child(2) > div > div > div > div > a.btn.btn-success").click()
time.sleep(3)

# masukkan username dan password 
driver.find_element(By.ID, "username").send_keys("aulia.maghfira")
driver.find_element(By.ID, "password").send_keys("4uL14m49h")

# click login
driver.find_element(By.ID, "kc-login").click()

time.sleep(5)

# click menu Data 
driver.find_element(By.CSS_SELECTOR, "body > div.app-body > div > nav > ul > li:nth-child(5) > a").click()
time.sleep(10)

# click menu Download
driver.find_element(By.CSS_SELECTOR, "body > div.app-body > div > nav > ul > li.nav-item.nav-dropdown.open > ul > li:nth-child(3) > a").click()

# download as csv 
# pilih kegiatan
driver.find_element(By.CSS_SELECTOR, "#app > div > div > div > div.card-body > div.container > div:nth-child(1) > div > select").click()
time.sleep(10)
driver.find_element(By.CSS_SELECTOR, "#app > div > div > div > div.card-body > div.container > div:nth-child(1) > div > select > option:nth-child(2)").click()
# pilih project 
driver.find_element(By.CSS_SELECTOR, "#app > div > div > div > div.card-body > div.container > div:nth-child(2) > div > select").click()
time.sleep(10)
driver.find_element(By.CSS_SELECTOR, "#app > div > div > div > div.card-body > div.container > div:nth-child(2) > div > select > option:nth-child(2)").click()
# pilih jenis data
driver.find_element(By.CSS_SELECTOR, "#app > div > div > div > div.card-body > div.container > div:nth-child(3) > div > select").click()
time.sleep(10)
driver.find_element(By.CSS_SELECTOR, "#app > div > div > div > div.card-body > div.container > div:nth-child(3) > div > select > option:nth-child(2)").click()
# pilih level cakupan 
driver.find_element(By.CSS_SELECTOR, "#app > div > div > div > div.card-body > div.container > div:nth-child(4) > div > select").click()
time.sleep(10)
driver.find_element(By.CSS_SELECTOR, "#app > div > div > div > div.card-body > div.container > div:nth-child(4) > div > select > option:nth-child(3)").click()
time.sleep(10)
# pilih prov
driver.find_element(By.CSS_SELECTOR, "#app > div > div > div > div.card-body > div.container > div:nth-child(8) > div > select").click()
time.sleep(10)
driver.find_element(By.CSS_SELECTOR, "#app > div > div > div > div.card-body > div.container > div:nth-child(8) > div > select > option:nth-child(2)").click()
# pilih kabkot
driver.find_element(By.CSS_SELECTOR, "#app > div > div > div > div.card-body > div.container > div:nth-child(9) > div > select").click()
time.sleep(10)

for i in range(2,12) : 
    j = str(i)
    driver.find_element(By.CSS_SELECTOR, "#app > div > div > div > div.card-body > div.container > div:nth-child(9) > div > select > option:nth-child("+j+")").click()
    # pilih kategori landmark 
    driver.find_element(By.CSS_SELECTOR, "#app > div > div > div > div.card-body > div.container > div:nth-child(13) > div > select").click()
    time.sleep(10)
    driver.find_element(By.CSS_SELECTOR, "#app > div > div > div > div.card-body > div.container > div:nth-child(13) > div > select > option:nth-child(3)").click()
    # download as
    driver.find_element(By.CSS_SELECTOR, "#app > div > div > div > div.card-footer > div > div > div > button").click()

    driver.find_element(By.CSS_SELECTOR, "body > div.swal2-container.swal2-center.swal2-backdrop-show > div > div.swal2-actions > button.swal2-confirm.swal2-styled").click()
    time.sleep(10)

    driver.find_element(By.CSS_SELECTOR, "body > div.swal2-container.swal2-center.swal2-backdrop-show > div > div.swal2-actions > button.swal2-confirm.swal2-styled").click()

driver.close()

# --------------------------------------------- #
#   CONVERT TEXT TO CSV
# --------------------------------------------- #

# import pandas as pd

# kode = ['01','02','03','04','05','09','11','71','72','74']

# for k in kode :
#     df = pd.read_csv('C:/Users/DELL/Downloads/12_landmark_64'+k+'.csv', delimiter=";")
#     df.to_csv('12_landmark_64'+k+'.csv')
    

# --------------------------------------------- #
# UPLOAD TO DRIVE
# --------------------------------------------- #
