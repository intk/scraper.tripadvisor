# Import libraries
import time
import json
import os
import re
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

# Get amount of pages
pageAmount = int(driver.find_elements_by_xpath("//a[contains(@class, 'pageNum cx_brand_refresh_phase2')]")[-1].text)


# function to check if the button is on the page, to avoid miss-click problem
def check_exists_by_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

# Push data to JSON file
def pushToJSON(data, file):
	# If JSON file exists, add data to it. Otherwise create it.
	if os.path.isfile(file):
		with open(file, 'r') as json_file:
			jsonList = json.loads(json_file.read())
	else:
		jsonList = [];

	with open(file, 'w') as json_file:

		jsonList.append(data)
		json.dump(jsonList, json_file, indent=2)

def formatDate(string):
	if "jan." in string:
		string = string.replace('jan.', '01')
	if "feb." in string:
		string = string.replace('feb.', '02')
	if "mrt." in string:
		string = string.replace('mrt.', '03')
	if "apr." in string:
		string = string.replace('apr.', '04')
	if "mei" in string:
		string = string.replace('mei', '05')
	if "jun." in string:
		string = string.replace('jun.', '06')
	if "jul." in string:
		string = string.replace('jul.', '07')
	if "aug." in string:
		string = string.replace('aug.', '08')
	if "sep." in string:
		string = string.replace('sep.', '09')
	if "okt." in string:
		string = string.replace('okt.', '10')
	if "nov." in string:
		string = string.replace('nov.', '11')
	if "dec." in string:
		string = string.replace('dec.', '12')

	date = "01-{}".format(string.replace(' ', '-'))
	return date


# Get reviews from page
def getReviews(driver, iterations):

	reviews = []

	container = driver.find_elements_by_xpath("//div[contains(@class, 'location-review-card-Card__ui_card--2Mri0')]")
	num_page_items = len(container)

	# Loop all reviews on the page
	for j in range(num_page_items):

		try:

			# Review object
			review = {
			    "date": container[j].find_element_by_xpath(".//div[contains(@class, 'social-member-event-MemberEventOnObjectBlock__event_type--')]").text,
				"author": container[j].find_element_by_xpath(".//a[contains(@class, 'social-member-event-MemberEventOnObjectBlock__member--')]").text.replace("\n", ""),
				"title": container[j].find_element_by_xpath(".//a[contains(@class, 'location-review-review-list-parts-ReviewTitle__reviewTitleText--')]").text.replace("\n", ""),
				"link": container[j].find_element_by_xpath(".//a[contains(@class, 'location-review-review-list-parts-ReviewTitle__reviewTitleText--')]").get_attribute('href'),
				"avatar":  "",
				"rating": int(int(container[j].find_element_by_xpath(".//span[contains(@class, 'ui_bubble_rating bubble_')]").get_attribute('class').split('_')[3])/10),
				"comment": ""
			}

			# Expand review
			container[j].find_element_by_xpath(".//q[contains(@class, 'location-review-review-list-parts-ExpandableReview__reviewText--')]").click()
			
			# Add review comment
			review["comment"] = container[j].find_element_by_xpath(".//q[contains(@class, 'location-review-review-list-parts-ExpandableReview__reviewText--gOmRC')]").text.replace("\n", "")

			# Add review profile picture
			review["avatar"] = container[j].find_element_by_xpath(".//a[contains(@class, 'styleguide-avatar-Avatar__avatar--2NStU')]/img").get_attribute('src')
			
			# Find date in string
			review["date"] = formatDate(re.findall("[\\w.]+ \d{4}", review["date"])[0])

			reviews.append(review)

		except Exception as e:

			if iterations == 0:
				return reviews

			errorDict = {
				"Exception": str(e),
				"Iterations": iterations,
				"ReviewNumber": j
			}

			print(errorDict)

			iterations = iterations -1
			getReviews(driver, iterations)


	# Return reviews when no errors were found
	return reviews


# change the value inside the range to save more or less reviews
print (f"{pageAmount} pages will be parsed.")
for i in range(0,pageAmount):

	reviews = getReviews(driver, 10)
	pushToJSON(reviews, "output.json")
	
	if check_exists_by_xpath(".//a[contains(@class, 'ui_button nav next primary ')]"):
		driver.find_element_by_xpath(".//a[contains(@class, 'ui_button nav next primary ')]").click()

	time.sleep(1)

#Exit program
time.sleep(1)
driver.close()
