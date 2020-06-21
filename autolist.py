from pprint import pprint
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

service = Service('chromedriver')
service.start()
driver = webdriver.Remote(service.service_url)

url = 'https://www.autolist.com/listings#page=1&location=Cary%2C+NC&make={}&model={}&year_min={}&year_max={}'\
    .format('Mazda', 'MX-5+Miata', '2019', '2019')

browser = webdriver.Chrome('chromedriver')
browser.get(url)
vehicles = browser.find_element_by_id('vehicle-list')
data = []
for vehicle in vehicles.find_elements_by_class_name('vehicle-item-view'):
    link = vehicle.find_element_by_tag_name('a').get_attribute('href')
    info = vehicle\
        .find_element_by_class_name('details')\
        .find_element_by_tag_name('h3')
    description = info\
        .find_element_by_class_name('description')\
        .find_element_by_class_name('headline').text
    price = info\
        .find_element_by_class_name('pricing')\
        .find_element_by_class_name('headline').text
    data.append({'description': description, 'price': price, 'link': link})

print(data)