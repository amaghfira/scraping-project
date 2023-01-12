from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC  
from bs4 import BeautifulSoup
import openpyxl, time, datetime

now = datetime.datetime.now()
SSO_REFERRER = "https://sso.bps.go.id/auth/realms/pegawai-bps/protocol/openid-connect/auth?scope=profile-pegawai%2Cemail&response_type=code&approval_prompt=auto&redirect_uri=https%3A%2F%2Fwebmonitoring.bps.go.id%2F&client_id=03310-webmon-1kw"
file_out_name = "uploadcacah_%s_%s_%s"%(now.hour, now.minute, now.second)
#file_upload = "G:\\__ MY CODE\\py\\scrap-monitoring\\%s.xls"%(file_out_name)
file_upload_pencacahan = "G:\\__ MY CODE\\py\\scrap-monitoring\\myfile.xls"
file_upload_sosial = "G:\\__ MY CODE\\py\\scrap-monitoring\\myfile_sosial.xls"

nks_list = ['55023', '75044', '15004', '75030', '55010', '65035', '30005', '25244', 
        '55234', '55252', '65246', '50486', '50178', '40150', '50215', '50141', 
        '50170', '60261', '60221', '65047', '25058', '60233', '75086', '75107', 
        '65133', '55121', '55101', '45104', '65071', '70249', '35160', '65164', 
        '75168', '60073', '10075', '70109', '60369', '40371', '70424', '75211', 
        '15212', '60401', '50377', '20448', '70314', '10325', '50031', '70519', 
        '70524', '60511', '70559', '30594']
temp = []

def fetch_nks_ruta(nks_list):
    for nks in nks_list:
        print("Mengambil NKS (%d/52) : %s"%(len(nks_list), nks))
        d.get("https://webmonitoring.bps.go.id/sak/progress/pencacahan?wil=6401%s&view=tabel&tgl_his=2021-08-19#"%(nks))
        time.sleep(3)
        bs = BeautifulSoup(d.page_source, "html.parser")
        tabdiv = bs.find('table', {'id':'tabel-progress'})
        rowname = bs.find_all('td', {'class':'col-id'})
       #rowname = tabdiv.find_all('td', {'class':'col-id'})

        for r in rowname:
            rtext = r.get_text()

            json_fetch = {
                "nks": nks,
                "ruta": rtext
            }
            print(json_fetch)

#def - file exchange (gagal export file corrupt, jangan dipakai)
def xlsx_to_xls(inp, outp):
    workbook = openpyxl.load_workbook(inp)
    outf_xls = f"%s.xls"%(outp)
    workbook.save(outf_xls)

# AUTOMATE LOGIN ATTEMPT
def login_credentials(driver, sso_site, username, pwd):
    driver.get(sso_site)
    driver.find_element("id","username").send_keys(username)
    driver.find_element("id", "password").send_keys(pwd)
    driver.find_element("id", "password").send_keys(Keys.ENTER)

chrome_options = Options()
#chrome_options.add_argument("--headless") #turn on kalo mau headless
d = webdriver.Chrome("D:\AMAGHFIRA\monit-auto-uploader\chromedriver.exe") #path_to_your_chromedriver_or_gecko

time.sleep(2)
login_credentials(d, SSO_REFERRER, "aulia.maghfira", "123456789") #password sudah dihapus, silakan diganti

#XLSX TO XLS
#xlsx_to_xls("G:\\__ MY CODE\\py\\scrap-monitoring\\Template Siap Upload XLSX.xlsx", file_out_name)

urls = ["pencacahan", "penerimaan"]
for u in urls:
#UPLOAD PENCACAHAN
    d.get("https://webmonitoring.bps.go.id/sak/unggah/%s"%(u))
    time.sleep(1)
    d.find_element("xpath", '//*[@id="provinsi"]/option[2]').click()
    el1 = WebDriverWait(d, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="kabupaten"]/option[2]')))
    el1.click()
    WebDriverWait(d, 1).until(EC.presence_of_element_located((By.XPATH, '//*[@id="uploader"]/form/input[1]')))
    if u != "pencacahan": d.find_element("xpath", '//*[@id="uploader"]/form/input[1]').send_keys(file_upload_sosial)
    else: d.find_element_by_xpath('//*[@id="uploader"]/form/input[1]').send_keys(file_upload_pencacahan)
    time.sleep(1)
    d.find_element_by_xpath('//*[@id="uploader"]/form/button').click()
    WebDriverWait(d, 120).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/section[2]/div/div[2]/div[2]/div[2]')))
    time.sleep(4)
d.close()