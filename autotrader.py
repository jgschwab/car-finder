import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

chrome_options = Options()
# chrome_options.add_argument("--headless")
service = Service('chromedriver')
service.start()
driver = webdriver.Remote(service.service_url, options=chrome_options)

make, model, startYear, endYear, trim, transmission = 'MAZDA', 'MX-5+Miata', '2019', '2019', 'MIATA%7CClub', 'MAN'
zipCode, radius = '27511', '500'

url = 'https://www.autotrader.com/cars-for-sale/Used+Cars/' \
      '{}/{}/' \
      '?listingTypes=USED%2CNEW' \
      '&searchRadius={}' \
      '&zip={}' \
      '&marketExtension=include' \
      '&startYear={}' \
      '&endYear={}' \
      '&trimCodeList={}' \
      '&transmissionCodes={}' \
      '&isNewSearch=true' \
      '&sortBy=relevance' \
      '&numRecords=25' \
      '&firstRecord=0' \
      .format(make, model, radius, zipCode, startYear, endYear, trim, transmission)

driver.get(url)
time.sleep(1)
listings = driver.find_elements_by_xpath('//div[@data-cmp="inventoryListing"]')
ids = []
for listing in listings:
    ids.append(listing.get_attribute('id'))

service.stop()
service.start()
driver = webdriver.Remote(service.service_url, options=chrome_options)

for ID in ids:
    driver.get("https://www.autotrader.com/cars-for-sale/vehicledetails.xhtml?listingId={}"
               .format(ID))
    details = driver.find_elements_by_xpath('//li[@class="list-bordered list-condensed"]')
    for item in details:
        print(item.find_element_by_xpath('div/div').text)

service.stop()

