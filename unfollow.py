from selenium import webdriver
import os
import time
from creds import username, password

URL = "https://github.com/"
MIN_CONTRIBUTIONS = 100

driver_path = os.path.join(os.getcwd(), "driver", "geckodriver.exe")
browser = webdriver.Firefox()

# Delay timers
login_delay = 5
navigation_delay = 3
min_delay = 1    # delay after application


def login():
	print("logging in")
	browser.get(URL + "login")
	time.sleep(navigation_delay)
	username_field = browser.find_element_by_id("login_field")
	password_field = browser.find_element_by_id("password")
	login_btn = browser.find_element_by_xpath("/html/body/div[3]/main/div/div[4]/form/div/input[12]")

	username_field.send_keys(username)
	password_field.send_keys(password)
	login_btn.click()
	time.sleep(login_delay)

	# navigate to profile following
	# https://github.com/bing101?tab=following
	browser.get(URL + username + "?tab=following")
	time.sleep(navigation_delay)

def unfollow_accounts(min_cont):
	"""
		Function takes an argument, minimum contribution,
		i;e an integer specifying minimum acceptable contributions 
		from a user

		if user_contr < min_cont:
			unfollow user_contr
	
	"""
	base_url = browser.current_url
	try:
		#link_drivers = browser.find_elements_by_xpath("/html/body/div[4]/main/div[2]/div/div[2]/div[2]/div/div[2]/div[2]/a")
		link_drivers = browser.find_elements_by_xpath('.//span[@class = "Link--secondary pl-1"])')
		print(link_drivers)
		links = []   # list of html links of followed accounts
		for elem in link_drivers:
		    print(elem.text)
		# for l in link_drivers:
		# 	link = l.get_attribute('href')  # extract link from object
		# 	links.append(link)
		# print("Links")
		# print(links[:5])
	

	except Exception as e:
		print("Error")
		print(e)


def main():
	print("Bot Run . . .")
	login()
	unfollow_accounts(MIN_CONTRIBUTIONS)

if __name__ == '__main__':
	main()