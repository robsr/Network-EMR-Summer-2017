import numpy as np
import pandas as pd
import urllib
import bs4

#INITIAL PARAMETERS
cities = ['Bangalore','Chandigarh','Chennai','Delhi','Hyderabad','Kolkata','Pune'] 
pages_per_city = 1000                         #pages per city required to be scrapped from Practo                                    
hosp_per_page = 10


def make_links(cities):                      #function returns the list of links of all the hospitals
    cities_list = ['https://www.practo.com/'+city+'/hospitals' for city in cities]
    city_links_final = []
    for city_link in cities_list:
        city_all_links = [(city_link+'?page='+str(page)) for page in range(1,pages_per_city+1)]
        city_links_final.append(city_all_links)    
    return city_links_final

def make_dataframe(links):                   #returns the dataframe containing columns of name,city,location,# of doctors, # of beds
    cities_links = links
    
    df2,df3,df4,df5 = pd.DataFrame([]),pd.DataFrame([]),pd.DataFrame([]),pd.DataFrame([])
    
    for city,city_name in zip(cities_links,cities):
            print(city_name)                 #to check the status of the execution
            for city_page in city:
                city_page_html = urllib.request.urlopen(city_page).read()
                city_page_soup = bs4.BeautifulSoup(city_page_html,'lxml')
    
                #Hospital NAMES
                names = [str(hospital.text)[:len(str(hospital.text))-17] for hospital in city_page_soup.find_all('h2')[1:]]
                if(names==[]):          #Condition to take all inputs
                    break
                df2_temp = pd.DataFrame(names)
                df2 = df2.append(df2_temp)
                
                #Location
                span_tags = city_page_soup.find_all('span',attrs={'itemprop':'addressLocality'})
                locations = [str(location.text)+', '+city_name for location in span_tags]
                df3_temp = pd.DataFrame(locations)
                df3 = df3.append(df3_temp)
                
                #number of doctors
                req_tags = city_page_soup.find_all('p',attrs={'class':'estab-col'})
                numbers = [str(number.text) for number in req_tags if 'Doctor' in number.text]
                for i in range(len(numbers)):
                    numbers[i] = int(''.join(c for c in numbers[i] if c.isdigit()))            
                
                df4_temp = pd.DataFrame(numbers)
                df4 = df4.append(df4_temp)
                
                #no.of beds
                link_tags = city_page_soup.find_all('a',attrs={'itemprop':'url'})
                link_tags = link_tags[:len(link_tags)-1]
                hosp_urls = [link.get('href') for link in link_tags]
                beds = []
                for url in hosp_urls:
                    try:           
                        hosp_html = urllib.request.urlopen(url).read()
                        hosp_soup = bs4.BeautifulSoup(hosp_html,'lxml')
                        
                        div_tags = hosp_soup.find_all('div',{'class':'hospital-data-col-left rating-column'})    
                        string = div_tags[0].text
                        bedno = int(''.join(c for c in string if c.isdigit()))
                        beds.append(bedno)
                    # handling exception when # of beds are not available    
                    except IndexError:
                        beds.append(np.NaN)
                
                df5_temp = pd.DataFrame(beds)
                df5 = df5.append(df5_temp)
            
                
    df2.reset_index(list(range(pages_per_city*hosp_per_page*len(cities))),drop=True, inplace=True)
    df3.reset_index(list(range(pages_per_city*hosp_per_page*len(cities))),drop=True, inplace=True)
    df4.reset_index(list(range(pages_per_city*hosp_per_page*len(cities))),drop=True, inplace=True)
    df5.reset_index(list(range(pages_per_city*hosp_per_page*len(cities))),drop=True, inplace=True)
    
    df = pd.concat([df2,df3,df4,df5], axis=1)
    df.columns = [['HOSPITAL NAME','LOCATION','NO. OF DOCTORS','NO. OF BEDS']]
    return df


# MAIN PROGRAMME
city_links = make_links(cities)
df = make_dataframe(city_links)
df.to_csv('hospitals.csv',header=True)







