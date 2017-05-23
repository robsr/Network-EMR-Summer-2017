import numpy as np
import pandas as pd
import urllib
import bs4

#INITIAL PARAMETERS
cities = ['Bangalore','Chandigarh','Chennai','Delhi','Hyderabad','Kolkata','Pune'] 
pages_per_city = 1                         #pages per city required to be scrapped from Practo                                    
hosp_per_page = 10                         #max no. of hospitals in a practo webpage

def make_links(cities):                      #function returns the list of links of all the hospitals
    cities_list = ['https://www.practo.com/'+city+'/hospitals' for city in cities]
    city_links_final = []
    for city_link in cities_list:
        city_all_links = [(city_link+'?page='+str(page)) for page in range(1,pages_per_city+1)]
        city_links_final.append(city_all_links)    
    return city_links_final


cities_links = make_links(cities)
print(cities_links)

df1,df2,df3,df4,df5,df6 = pd.DataFrame([]),pd.DataFrame([]),pd.DataFrame([]),pd.DataFrame([]),pd.DataFrame([]),pd.DataFrame([])

for city in cities_links:
        for city_page in city:
            city_page_html = urllib.request.urlopen(city_page).read()
            city_page_soup = bs4.BeautifulSoup(city_page_html,'lxml')

            #grabbing hospitals links
            a_tags = city_page_soup.find_all('a', attrs={'itemprop':'url'})
            hosp_links = [tag.get('href') for tag in a_tags[:len(a_tags)-1]]
            
            #doctor names and experience
            for link in hosp_links:
                hosp_page_html = urllib.request.urlopen(link).read()
                hosp_page_soup = bs4.BeautifulSoup(hosp_page_html,'lxml')
                
                #Doctor's Name
                dr_tags = hosp_page_soup.find_all('h2', attrs={'itemprop':'name'})  #tags  containing Dr.'s name
                dr_names = [tag.text for tag in dr_tags if 'Dr.' in tag.text]
                df1_temp = pd.DataFrame(dr_names)
                df1 = df1.append(df1_temp)
                
                #Doctor's Experience
                exp_tags = hosp_page_soup.find_all('p', attrs={'class':'doc-exp-years'}) #tags containing Dr.'s experience
                dr_exp = [tag.text for tag in exp_tags]
                for i in range(len(dr_exp)):
                    dr_exp[i] = int(''.join(c for c in dr_exp[i] if c.isdigit()))
                df2_temp = pd.DataFrame(dr_exp)
                df2 = df2.append(df2_temp)
                
                #Hospital's Name
                hosp_name_temp = hosp_page_soup.find('h1').text        #tag containing hospital name
                df3_temp = [hosp_name_temp]*len(df1_temp)              #repeating hospital name to make a dataframe
                df3 = df3.append(df3_temp)
                
                #Doctor's Qualifications
                dr_qual_tags = hosp_page_soup('p',attrs={'class':'doc-qualifications'}) #tags for all the qualifications
                qualifications = []
                for dr_qual_tag in dr_qual_tags:
                    string = '' 
                    for span_tag in dr_qual_tag.find_all('span'):            #joining the qualifications of a doctor in a single string
                         string = string + (span_tag.text+', ')
                
                    string = string[:len(string)-2]
                    qualifications.append(string) 
 
                df4_temp = pd.DataFrame(qualifications)
                df4 = df4.append(df4_temp)                
                
                #Specialization
                
                #City
                hosp_loc_temp = hosp_page_soup.find('h2',attrs={'class':'clinic-location'}).text   #tag containing hospital's Location
                df6_temp = [hosp_loc_temp]*len(df1_temp)              
                df6 = df6.append(df6_temp)
                



#df2.reset_index(list(range(pages_per_city*hosp_per_page*len(cities))),drop=True, inplace=True)
#print(len(list(range(pages_per_city*hosp_per_page*len(cities)))))
#df3.reset_index(list(range(pages_per_city*hosp_per_page*len(cities))),drop=True, inplace=True)
#df4.reset_index(list(range(pages_per_city*hosp_per_page*len(cities))),drop=True, inplace=True)
#df5.reset_index(list(range(pages_per_city*hosp_per_page*len(cities))),drop=True, inplace=True)
#
#df = pd.concat([df2,df3,df4,df5], axis=1)
#df.columns = [['NAME','EXPERIENCE(years)','HOSPITAL NAME','SPECIALIZATION','CITY']]

