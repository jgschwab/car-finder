import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

manual = True

chrome_options = Options()
# chrome_options.add_argument("--headless")
service = Service('chromedriver')
service.start()
driver = webdriver.Remote(service.service_url, options=chrome_options)

url = 'https://www.autolist.com/listings#page=1'\
      '&location={}%2C+{}'\
      '&make={}'\
      '&model={}'\
      '&year_min={}'\
      '&year_max={}'\
      '&radius={}'\
      '&trim[]={}'\
      '&transmission[]={}'\
      .format('Cary', 'NC', 'Mazda', 'MX-5+Miata', '2019', '2019', 'Any', 'Club', 'manual')

driver.get(url)
vehicles = driver.find_element_by_id('vehicle-list')
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

for car in data:
    link = car['link']
    driver.get(link)
    print(link)
    time.sleep(.5)
    driver.find_element_by_xpath("//a[@data-action='extra details']").click()
    time.sleep(1)
    color = vin = None
    features = driver.find_elements_by_class_name("vehicle-feature")

    for feature in features:
        if vin is None and feature.find_element_by_class_name("feature-label").text == "VIN":
            vin = feature.find_element_by_class_name("feature-value").text
        elif color is None and feature.find_element_by_class_name("feature-label").text == "Exterior Color":
            color = feature.find_element_by_class_name("feature-value").text
        else:
            continue
        if None not in [color, vin]:
            break
    assert None not in [color, vin]

    car['VIN'] = vin
    car['color'] = color

print(data)
service.stop()
