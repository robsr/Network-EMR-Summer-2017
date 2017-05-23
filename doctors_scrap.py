import pandas as pd
import urllib
import bs4
import re

#INITIAL PARAMETERS
#cities = ['Bangalore','Chandigarh','Chennai','Delhi','Hyderabad','Kolkata','Pune']
cities = ['Bangalore','Delhi'] 
pages_per_city = 1                         #pages per city required to be scrapped from Practo                                    
hosp_per_page = 10                         #max no. of hospitals in a practo webpage

def make_links(cities):                      #function returns the list of links of all the hospitals
    cities_list = ['https://www.practo.com/'+city+'/hospitals' for city in cities]
    city_links_final = []
    for city_link in cities_list:
        city_all_links = [(city_link+'?page='+str(page)) for page in range(1,pages_per_city+1)]
        city_links_final.append(city_all_links)    
    return city_links_final


def verified_doc_links(hosp_page_soup):     #function that returns verified doctor links from the hospital webpage
    doc_links = [doc_link_tag.get('href') for doc_link_tag in hosp_page_soup.find_all('a', attrs={'class':'link doc-name'})]
    ver_doc_links = []
    
    for doc_link in doc_links:
        doc_page_html = urllib.request.urlopen(doc_link).read()
        doc_page_soup = bs4.BeautifulSoup(doc_page_html,'lxml')
        
        ver_label = doc_page_soup.find('span', attrs={'class':'verification-label'})
        
        if ver_label != None:
            ver_doc_links.append(doc_link)
    return ver_doc_links



cities_links = make_links(cities)
df1,df2,df3,df4,df5 = pd.DataFrame([]),pd.DataFrame([]), pd.DataFrame([]), pd.DataFrame([]), pd.DataFrame([])

for city in cities_links:
        for city_page in city:
            city_page_html = urllib.request.urlopen(city_page).read()
            city_page_soup = bs4.BeautifulSoup(city_page_html,'lxml')

            #grabbing hospitals links
            a_tags = city_page_soup.find_all('a', attrs={'itemprop':'url'})
            hosp_links = [tag.get('href') for tag in a_tags[:len(a_tags)-1]]
            for hosp_link in hosp_links:                    
                hosp_page_html = urllib.request.urlopen(hosp_link).read()
                hosp_page_soup = bs4.BeautifulSoup(hosp_page_html,'lxml')
                
                verified_links = verified_doc_links(hosp_page_soup)
                no_of_ver_doctors = len(verified_links)
                dr_names, dr_qual_strings, dr_exp_strings, exp_yrs, spec_strings = [],[],[],[],[]
                
                for ver_doc_link in verified_links:    
                    doc_page_html = urllib.request.urlopen(ver_doc_link).read()
                    doc_page_soup = bs4.BeautifulSoup(doc_page_html,'lxml')
                    
                    #doctor name    
                    dr_name = doc_page_soup.find('h1').get('title')
                    dr_names.append(dr_name)
                    
                    #doctor speciality and experience(in years)
                    dr_exp_string = doc_page_soup.find('h2',attrs={'class':'doctor-specialties'}).text
                    dr_exp_string = dr_exp_string.replace('\n','')
                    dr_exp_string = dr_exp_string.replace('\t','')
                    
                    strings = dr_exp_string.split(',')
                    result = re.findall(r'[0-9]+', strings[len(strings)-1])
                    result_int = map(int,result)
                    result_int = [int(string) for string in result_int]
                    exp_yrs.append(result_int)
                    
#                    strings = strings[:len(strings)-1]
#                    strings = [string.replace(' ','') for string in strings]
#                
#                    spec_string = strings[0]
#                    for string in strings[1:]:
#                        spec_string = spec_string + ', ' + string
#                    spec_strings.append(spec_string)        
                    
                    #doctor qualifications
                    dr_qual_string = doc_page_soup.find('p',attrs={'class':'doctor-qualifications'}).text
                    dr_qual_string = dr_qual_string.replace('\n','')
                    dr_qual_string = dr_qual_string.replace('\t','')
                    dr_qual_strings.append(dr_qual_string)
        
    
                df1_temp = pd.DataFrame(dr_names)
                df1 = df1.append(df1_temp)
                
                df2_temp = pd.DataFrame(exp_yrs)
                df2 = df2.append(df2_temp)
                
#                df3_temp = pd.DataFrame(spec_strings)
#                df3 = df3.append(df3_temp)
                
                df4_temp = pd.DataFrame(dr_qual_strings)
                df4 = df4.append(df4_temp)
                
                #hospital name
                hosp_name_temp = hosp_page_soup.find('h1').text            #tag containing hospital name
                df5_temp = [hosp_name_temp]*no_of_ver_doctors              #repeating hospital name to make a dataframe
                df5 = df5.append(df5_temp)

                



#df2.reset_index(list(range(pages_per_city*hosp_per_page*len(cities))),drop=True, inplace=True)
#print(len(list(range(pages_per_city*hosp_per_page*len(cities)))))
#df3.reset_index(list(range(pages_per_city*hosp_per_page*len(cities))),drop=True, inplace=True)
#df4.reset_index(list(range(pages_per_city*hosp_per_page*len(cities))),drop=True, inplace=True)
#df5.reset_index(list(range(pages_per_city*hosp_per_page*len(cities))),drop=True, inplace=True)
#
#df = pd.concat([df2,df3,df4,df5], axis=1)
#df.columns = [['NAME','EXPERIENCE(years)','HOSPITAL NAME','SPECIALIZATION','CITY']]

