from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC  
from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup
import openpyxl, time, datetime


now = datetime.datetime.now()

driver = webdriver.Chrome("D:\AMAGHFIRA\python-project\scrapregsosek\chromedriver.exe") #path_to_your_chromedriver_or_gecko

# driver.get("https://drive.google.com")
driver.get("https://accounts.google.com/v3/signin/identifier?dsh=S2131278869%3A1666321790662179&continue=http%3A%2F%2Fdrive.google.com%2F%3Futm_source%3Den&ltmpl=drive&passive=true&service=wise&usp=gtd&utm_campaign=web&utm_content=gotodrive&utm_medium=button&flowName=GlifWebSignIn&flowEntry=ServiceLogin&ifkv=AQDHYWpdr5tGw6IrQPuByln-Ez4ijCsFQsKIYPWsz3GXYwxVYCEAFMc6WzDU2EKURcFZLEhg2eBuGw")
driver.maximize_window()

driver.implicitly_wait(10)

# login dulu 
username = driver.find_element(By.XPATH, '//*[@id="identifierId"]')
username.send_keys("admin@bpskaltim.id")
username.send_keys(Keys.ENTER)

driver.implicitly_wait(10)

pwd = driver.find_element(By.CSS_SELECTOR, "#password > div.aCsJod.oJeWuf > div > div.Xb9hP > input")
pwd.send_keys("@m3nc4t4tIDN")
pwd.send_keys(Keys.ENTER)

driver.implicitly_wait(10)

# masuk folder pemetaan
act = ActionChains(driver)

driver.find_element(By.CSS_SELECTOR, "#nt\:Dr > div.a-U-J.a-U-xc-J > div.a-U-Ze-j.a-U-ye-jm > div > div.a-U-Ze-c-Vf > svg").click()
driver.find_element(By.CSS_SELECTOR, "#nt\:Dr\;1x > div.a-U-J > div.a-U-Ze-j.a-U-ye-jm > div > div.a-U-Ze-c-Vf > svg").click()
driver.find_element(By.CSS_SELECTOR, "#nt\:Dr\;1x\;10\:label > div > span").click()

# click add 
driver.find_element(By.CSS_SELECTOR, "#drive_main_page > div > div.ZHllM > div > button.brbsPe.Ss7qXc.a-qb-d").click()


# to be continued... gatau gmn cara upload multiple files wkwk