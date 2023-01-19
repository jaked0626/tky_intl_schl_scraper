############################################################
# intl_schools_tky.py: 
#   crawls https://www.international-schools-database.com/in/tokyo to get market size 
# purpose:
#   research market size
############################################################

PAGE_URL = "https://www.international-schools-database.com/in/tokyo"

import requests
from bs4 import BeautifulSoup
from time import sleep
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

def make_soup(url):
    # Make the request, using headers to mask crawler
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    response = requests.get(url, headers=headers)

    # Create the Beautiful Soup object
    soup = BeautifulSoup(response.content, 'html.parser')

    return soup

def get_school_panels(soup):
    h2_elements = soup.find_all('h2', class_='card-row-title school-name')
    return h2_elements

def extract_schoolname_link(school_element):
    name = ""
    link = ""
    a_element = school_element.find('a', href=True)
    if a_element:
        link = a_element['href']
        # Get the text
        name = a_element.text
    
    return name, link

def extract_school_info(soup):
    currencies = soup.find_all('span', class_="currency")
    fee_lb = currencies[0].text
    fee_ub = currencies[1].text
    table_soup = soup.find("table", class_="table background-color dark questionnaire-table")
    student_body = table_soup.find("p").text
    return fee_lb, fee_ub, student_body

def crawl_main():
    df_cols = ['school_name', 'tuition_range', 'number_of_students']
    with open("./crawled_data/intl_school_students.csv", "w") as f:
        f.write(",".join(df_cols) + "\n")

    # requests doesnt work
    # page_soup = make_soup(PAGE_URL)
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(PAGE_URL)
    sleep(1)
    page_soup = BeautifulSoup(driver.page_source, 'html.parser')
    school_panels = get_school_panels(page_soup)

    for school in school_panels:
        name, link = extract_schoolname_link(school)
        driver.get(link)
        sleep(3)
        school_soup = BeautifulSoup(driver.page_source, "html.parser")
        fee_lb, fee_ub, student_body = extract_school_info(school_soup)
        fee_range = f"{fee_lb}~{fee_ub}".replace(",", "")
        # write to csv file 
        with open("./crawled_data/intl_school_students.csv", "a") as f:
            f.write(",".join([name, fee_range, student_body]) + "\n")
        
if __name__ == "__main__":
    crawl_main()