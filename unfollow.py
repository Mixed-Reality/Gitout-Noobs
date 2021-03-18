from selenium import webdriver
import os
import time
from creds import username, password
import re
import bs4 as bs
import urllib.request

URL = "https://github.com/"
MIN_CONTRIBUTIONS = 100

driver_path = os.path.join(os.getcwd(), "driver", "geckodriver.exe")
browser = webdriver.Firefox()

# Delay timers
login_delay = 5
navigation_delay = 2
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
	
def get_follower_list(url):
	"""
		Function takes the link of followers list page 
		and extracts the usernames from the list
		return a list of usernames which you follow
	
	"""

	print("getting following list")
	source = urllib.request.urlopen(url).read()
	soup = bs.BeautifulSoup(source,'lxml')

	# check if follwed account list has ended
	list_end = soup.find('p', {'class': 'mt-4'})
	if list_end and (list_end.get_text().find("You've reached the end of")):
		print("List ends")
		return None


	# xml of all the username list
	spans = soup.find_all('span', {'class' : 'Link--secondary pl-1'})
	username_list = [span.get_text() for span in spans]
	return username_list


def unfollow_accounts(min_cont, username=username):
	"""
		Function takes an argument, minimum contribution,
		i;e an integer specifying minimum acceptable contributions 
		from a user

		if user_contr < min_cont:
			unfollow user_contr
	
	"""
	print(username)
	curr_page = 2    # list of followed accounts page number 
	curr_url = URL + username + "?tab=following"
	browser.get(curr_url)
	time.sleep(navigation_delay)
	try:
		while True:
			
			curr_url =  f"{URL}{username}?&tab=following" if curr_page == 1 else f"{URL}{username}?page={curr_page}&tab=following"
			print("Current url: ", curr_url)

			usernames = get_follower_list(curr_url)

			# list ended
			if not usernames:
				return

			for username in usernames:
				acc_link = URL + username  # link of the account 

				source = urllib.request.urlopen(acc_link).read()
				soup = bs.BeautifulSoup(source,'lxml')

				browser.get(acc_link)
				time.sleep(navigation_delay)
				contributions = (soup.find('h2', {'class': 'f4 text-normal mb-2'}).get_text()).split()[0]
				contributions = int(contributions.replace(",", ""))
				# contributions = browser.find_element_by_class_name("f4 text-normal mb-2")
				print(f"{username} has {contributions} contributions")
				# unfollow
				if(contributions < min_cont):
					# unfollow_btn = browser.find_elements_by_xpath("/html/body/div[4]/main/div[2]/div/div[1]/div/div[3]/div[1]/div/div[1]/span/form[2]/input[2]")
					# unfollow_btn = browser.find_element_by_name("commit")
					# unfollow_btn = browser.find_element_by_class_name("btn btn-block")
					# unfollow_btn = browser.find_element_by_xpath("//*[contains(text(), 'Unfollow')]")
					unfollow_btn = browser.find_elements_by_xpath("//input[@aria-label='Unfollow this person']")
					# print(unfollow_btn)
					#  /html/body/div[4]/main/div[2]/div/div[1]/div/div[3]/div[1]/div/div[1]/span/form[2]/input[2]
					# unfollow_btn = browser.find_element_by_class_name("btn btn-block")			
					# unfollow_btn.click()

					try:
						print("Unfollowing")
						for i in unfollow_btn:
							i.submit()
					except:
						pass
			curr_page += 1

	
	except Exception as e:
		print("Error")
		print(e)


def main():
	print("Bot Run . . .")
	login()
	unfollow_accounts(MIN_CONTRIBUTIONS)


if __name__ == '__main__':
	main()