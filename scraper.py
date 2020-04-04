# Import libraries
import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

# Run Headless Chrome
options = Options()  
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
options.add_argument("--disable-gpu")
options.headless = False

# Enable usage of cache and cookies
options.add_argument('user-data-dir=data')

# import the webdriver, chrome driver is recommended
driver = webdriver.Chrome('./chromedriver', options=options)

# insert the tripadvisor's website of one attraction 
driver.get("https://www.tripadvisor.nl/Attraction_Review-g188582-d319468-Reviews-Van_Abbemuseum-Eindhoven_North_Brabant_Province.html")


# function to check if the button is on the page, to avoid miss-click problem
def check_exists_by_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

def formatDate(string):
	if "januari" in string:
		string = string.replace('januari', '01')
	if "februari" in string:
		string = string.replace('februari', '02')
	if "maart" in string:
		string = string.replace('maart', '03')
	if "april" in string:
		string = string.replace('april', '04')
	if "mei" in string:
		string = string.replace('mei', '05')
	if "juni" in string:
		string = string.replace('juni', '06')
	if "juli" in string:
		string = string.replace('juli', '07')
	if "augustus" in string:
		string = string.replace('augustus', '08')
	if "september" in string:
		string = string.replace('september', '09')
	if "oktober" in string:
		string = string.replace('oktober', '10')
	if "november" in string:
		string = string.replace('november', '11')
	if "december" in string:
		string = string.replace('december', '12')

	date = "01-{}".format(string.replace(' ', '-'))
	return date


# Get reviews from page
def getReviews(driver, iterations):

	container = driver.find_elements_by_xpath("//div[contains(@class, 'location-review-card-Card__ui_card--2Mri0')]")
	num_page_items = len(container)

	# Loop all reviews on the page
	for j in range(num_page_items):

		try:

			# Review object
			review = {
			    "date": container[j].find_element_by_xpath(".//span[contains(@class, 'location-review-review-list-parts-EventDate__event_date--1epHa')]").text.replace('Datum van activiteit: ', ""),
				"author": container[j].find_element_by_xpath(".//a[contains(@class, 'social-member-event-MemberEventOnObjectBlock__member--')]").text.replace("\n", ""),
				"title": container[j].find_element_by_xpath(".//a[contains(@class, 'location-review-review-list-parts-ReviewTitle__reviewTitleText--')]").text.replace("\n", ""),
				"link": container[j].find_element_by_xpath(".//a[contains(@class, 'location-review-review-list-parts-ReviewTitle__reviewTitleText--')]").get_attribute('href'),
				"rating": int(int(container[j].find_element_by_xpath(".//span[contains(@class, 'ui_bubble_rating bubble_')]").get_attribute('class').split('_')[3])/10),
				"comment": ""
			}

			# Expand review
			container[j].find_element_by_xpath(".//q[contains(@class, 'location-review-review-list-parts-ExpandableReview__reviewText--')]").click()
			# Add review comment
			review["comment"] = container[j].find_element_by_xpath(".//q[contains(@class, 'location-review-review-list-parts-ExpandableReview__reviewText--gOmRC')]").text.replace("\n", "")
			review["date"] = formatDate(review["date"])
			print(review)

		except:

			if iterations == 0:
				return False

			print(f"EXCEPT, Iterations: {iterations}")
			iterations = iterations -1
			return getReviews(driver, iterations)

	return True


# change the value inside the range to save more or less reviews
for i in range(0,10):

	if getReviews(driver, 10) == False:
		print (f"Couldn't parse page #{i}")

	driver.find_element_by_xpath(".//a[contains(@class, 'ui_button nav next primary ')]").click()
	print(f"PAGE #{i}")

#Exit program
time.sleep(1)
driver.close()




