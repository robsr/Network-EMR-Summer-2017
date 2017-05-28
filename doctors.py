import pandas as pd
import urllib
import bs4
import re
import numpy as np

a=0
#df = pd.read_csv("./Data/sample_hospi")
df=['https://www.practo.com/bangalore/hospital/people-tree-hospitals-yeshwanthpur-1','https://www.practo.com/bangalore/hospital/marvel-speciality-hospital-and-fertility-centre-koramangala-1-block']
df1, df2, df3, df4, df5 = pd.DataFrame([]), pd.DataFrame([]), pd.DataFrame([]), pd.DataFrame([]), pd.DataFrame([])
for link in df:
    hospi_page = urllib.request.urlopen(link).read()
    hosp_soup = bs4.BeautifulSoup(hospi_page, 'lxml')
    doc_links = [doc_link_tag.get('href') for doc_link_tag in hosp_soup.find_all('a', attrs={'class':'link doc-name'})]

    ds = [d.get('href') for d in hosp_soup.find_all('a', attrs={'class':'page_link'})]

    for doc_link in doc_links:
        a+=1
        doc_page_html = urllib.request.urlopen(doc_link).read()
        doc_page_soup = bs4.BeautifulSoup(doc_page_html,'lxml')

        #doctor's name
        dr_name = doc_page_soup.find('h1').get('title')
        df1_temp = pd.DataFrame([dr_name])
        df1=df1.append(df1_temp)

        #doctor qualifications
        dr_qual_string = doc_page_soup.find('p',attrs={'class':'doctor-qualifications'}).text
        dr_qual_string = dr_qual_string.replace('\n','')
        dr_qual_string = dr_qual_string.replace('\t','')
        
        df2_temp=pd.DataFrame([dr_qual_string])
        df2=df2.append(df2_temp)

        #doctor speciality and experience(in years) 
        dr_exp_string = doc_page_soup.find('h2',attrs={'class':'doctor-specialties'}).text
        dr_exp_string = dr_exp_string.replace('\n','')
        dr_exp_string = dr_exp_string.replace('\t','')

        strings = dr_exp_string.split(',')
        result = re.findall(r'[0-9]+', strings[len(strings)-1])
        result_int = map(int,result)
        result_int = [int(string) for string in result_int]
        df3_temp=pd.DataFrame([result_int])
        df3=df3.append(df3_temp)
        
        strings = strings[:len(strings)-1]
        strings = [string.replace(' ','') for string in strings]
    
        if len(strings) != 0 :
            spec_string = strings[0]
            for i in range(1,len(strings)):
                spec_string = spec_string + ', ' + strings[i]
            df4_temp=pd.DataFrame([spec_string])
            df4=df4.append(df4_temp)

        else :
            df4=df4.append(np.NaN)
        
        #hospi name
        hosp_name_temp = hosp_soup.find('h1').text
        df5_temp=pd.DataFrame([hosp_name_temp])
        df5=df5.append(df5_temp)

df1.reset_index(list(range(a)),drop=True, inplace=True)
df2.reset_index(list(range(a)),drop=True, inplace=True)
df3.reset_index(list(range(a)),drop=True, inplace=True)
df4.reset_index(list(range(a)),drop=True, inplace=True)
df5.reset_index(list(range(a)),drop=True, inplace=True)

df = pd.concat([df1,df2,df5,df3,df4], axis=1)
df.columns = [['NAME','QUALIFICATIONS','SPECIALIZATION','EXPERIENCE(years)','HOSPITAL NAME']]

df.to_csv('Doc.csv',header=True)