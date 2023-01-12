# --------------------------------------------- #
#   CONVERT TEXT TO CSV
# --------------------------------------------- #

import pandas as pd

kode = ['01','02','03','04','05','09','11','71','72','74']

for k in kode :
    df = pd.read_csv('C:/Users/DELL/Downloads/12_landmark_64'+k+'.csv', delimiter=";")
    df.to_csv('12_landmark_64'+k+'.csv')