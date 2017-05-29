import pandas as pd
import urllib
import bs4
import re
import numpy as np

df=['https://www.practo.com/bangalore/hospital/people-tree-hospitals-yeshwanthpur-1?page=4&ajax=true']
df1, df2, df3, df4 = pd.DataFrame([]), pd.DataFrame([]), pd.DataFrame([]), pd.DataFrame([])
a=0
for link in df:
    a+=1
    hospi_page = urllib.request.urlopen(link).read()
    hospi_html = bs4.BeautifulSoup(hospi_page, 'lxml')

    #doctor name
    dr_name = hospi_html.find('h2').text
    df1_temp=pd.DataFrame([dr_name])
    df1=df1.append(df1_temp)
    
    #doctor experience
    dr_exp = hospi_html.find('p',attrs = {'class':'doc-exp-years'}).text
    exp = [int(s) for s in dr_exp.split() if s.isdigit()]
    df2_temp=pd.DataFrame(exp)
    df2=df2.append(df2_temp)
    
    #doctor Qualification
    dr_qual_raw = hospi_html.find('p', attrs = {'class':'doc-qualifications'}).text
    dr_qual_raw = dr_qual_raw.replace('\n','')
    print(dr_qual_raw)
    df3_temp=pd.DataFrame([dr_qual_raw])
    df3=df3.append(df3_temp)

    #doctor Specialties
    dr_spec_raw = hospi_html.find('p', attrs = {'class':'doc-specialties'}).text
    dr_spec_raw = dr_spec_raw.replace('\n','')
    dr_spec = dr_spec_raw.replace(' ','')
    df4_temp = pd.DataFrame([dr_spec])
    df4=df4.append(df4_temp)

df1.reset_index(list(range(a)), drop=True, inplace=True)
df2.reset_index(list(range(a)), drop=True, inplace=True)
df3.reset_index(list(range(a)), drop=True, inplace=True)
df4.reset_index(list(range(a)), drop=True, inplace=True)

df = pd.concat([df1,df2,df3,df4], axis=1)
df.columns = [['NAME','EXPERIENCE','QUALIFICATION','SPECIALTIES']]

df.to_csv('Doc_FINAL.csv',header=True)
