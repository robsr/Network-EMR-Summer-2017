import pandas as pd
import urllib
import bs4
import re
import numpy as np

links=pd.read_csv('Data_set.csv').LINKS     #use the address of the csv file if not present in same directory.
hosp_name=pd.read_csv('Data_set.csv')['HOSPITAL NAME']
df1, df2, df3, df4, df5 = pd.DataFrame([]), pd.DataFrame([]), pd.DataFrame([]), pd.DataFrame([]), pd.DataFrame([])
a=0
for link,hospital in zip(links,hosp_name):
    for i in range(1,100):
        link_f=link +'?page='+str(i)+'&ajax=true'
        print(link_f)
        hospi_page = urllib.request.urlopen(link_f).read()
        hospi_html = bs4.BeautifulSoup(hospi_page, 'lxml')

        #doctor name
        dr_tags = hospi_html.find_all('h2')
        if (dr_tags==[]):
            break
        dr_names = [tag.text for tag in dr_tags]
        df1_temp=pd.DataFrame(dr_names)
        df1=df1.append(df1_temp)
        a+=len(df1_temp)
        
        #doctor experience
        dr_exp_tag = hospi_html.find_all('p',attrs = {'class':'doc-exp-years'})
        dr_exps = [tag.text for tag in dr_exp_tag]
        for dr_exp in dr_exps:
            exp = [int(s) for s in dr_exp.split() if s.isdigit()]
            df2_temp=pd.DataFrame(exp)
            df2=df2.append(df2_temp)
        
        #doctor Qualification
        dr_qual_raw = hospi_html.find_all('p', attrs = {'class':'doc-qualifications'})
        dr_qual = [tag.text for tag in dr_qual_raw]
        dr_qual_final = [a.replace('\n','') for a in dr_qual]
        df3_temp = pd.DataFrame(dr_qual_final)
        df3=df3.append(df3_temp)

        #doctor Specialties
        dr_spec_raw = hospi_html.find_all('p', attrs = {'class':'doc-specialties'})
        dr_spec = [tag.text for tag in dr_spec_raw]
        dr_spec_final = [a.replace('\n','') for a in dr_spec]
        dr_spec_final2 = [a.replace(' ','') for a in dr_spec_final]
        df4_temp = pd.DataFrame(dr_spec_final2)
        df4=df4.append(df4_temp)

        #Hospital Name
        df5_temp = pd.DataFrame([hospital]*len(df1_temp))
        df5 = df5.append(df5_temp)



df1.reset_index(list(range(a)), drop=True, inplace=True)
df2.reset_index(list(range(a)), drop=True, inplace=True)
df3.reset_index(list(range(a)), drop=True, inplace=True)
df4.reset_index(list(range(a)), drop=True, inplace=True)
df5.reset_index(list(range(a)), drop=True, inplace=True)

df = pd.concat([df1,df2,df3,df4,df5], axis=1)
df.columns = [['NAME','EXPERIENCE','QUALIFICATION','SPECIALTIES','HOSPITAL']]

df.to_csv('Doc_sample.csv',header=True)
