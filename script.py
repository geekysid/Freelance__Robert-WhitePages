from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from colorama import init
from termcolor import cprint
from bs4 import BeautifulSoup
import pandas as pd
import time, json, os, sys, csv, re


# global variables
CONFIG_DATA = {}		# fata from config data
DATA = {}
PEOPLE_LIST = []
PERSON_DATA = []
PERSON_COUNT = 0
# PATH ='E:\\SIDDHANT\\Freelancing\\Robert\\WhitePages'


#  just fro decoration
def intro_deco():
	print("\n\n")
	print("\t", '#'*40)
	print("\t", "#                                      #")
	print("\t", "#        SCRAPER FOR WHITEPAGES        #")
	print("\t", "#           By: SIDDHANT SHAH          #")
	print("\t", "#             Dt: 11-11-2020           #")
	print("\t", "#     siddhant.shah.1986@gmail.com     #")
	print("\t", "#   **Just for Educational Purpose**   #")
	print("\t", "#                                      #")
	print("\t", '#'*40)
	print()


# getting information from config file
def initializer():
	global CONFIG_DATA
	global URL_SPECS

	if os.path.exists(f'config.json'):
		with open (f'config.json', 'r') as config_file:
			CONFIG_DATA = json.load(config_file)
	else:
		CONFIG_DATA = {}
		cprint('  [X] Config file not found. Terminating Script', 'red', attrs=['bold'])


# Setting up webdriver
def get_browser(headless=False):
	pathToChromeDriver = f"{CONFIG_DATA['path_to_chromedriver']}\\chromedriver"
	chrome_options = Options()

	# giving a higher resolution to headless browser so that click operation works
	if headless:
		chrome_options.headless = headless
	else:
		chrome_options.add_argument('--window-size=1920,1080')
		chrome_options.add_argument("--start-maximized")

	browser = webdriver.Chrome(executable_path = pathToChromeDriver, options=chrome_options)
	return browser


# reading input csv file
def read_input_csv():
	global CONFIG_DATA
	CONFIG_DATA['input'] = {}

	input_path = CONFIG_DATA['path_to_input_file']
	output_path = CONFIG_DATA['path_to_output_file']
	count = 0

	input_file = input('   [?] Please mention name of input csv file: ')
	# input_file = 'xyz.csv'

	if os.path.exists(f'{input_path}\\{input_file}'):

		if input_file.split(".")[-1] == 'csv':
			CONFIG_DATA['output_file'] = f'{output_path}\\{input_file.rsplit(".", 1)[0]}-output.csv'

			input_file = f'{input_path}\\{input_file}'

			with open(input_file, 'r') as input_data:
				for line in csv.DictReader(input_data):
					CONFIG_DATA['input'][count] = line
					count += 1

			return True
		else:
			cprint(f'   [x] Input file {input_file} is not a csv. Terminating Program', 'red', attrs=['bold'])
			return False
	else:
		print(f'{input_path}\\{input_file}')
		print(os.getcwd())
		cprint(f'   [x] Input file {input_file} dosen\'t exists. Terminating Program.', 'red', attrs=['bold'])
		return False


def get_output_for_each_input():
	global PEOPLE_LIST
	input_data = CONFIG_DATA['input']

	for key in input_data.keys():
		surname = input_data[key]['surname']
		initial = input_data[key]['initial']
		location = input_data[key]['location']
		cprint(f'\n\n  QUERY \n  --> Surname: {surname} \n  --> Initial: {initial} \n  --> Location: {location} ', 'green', attrs=['bold'])

		enter_input_data(surname, initial, location)
		PEOPLE_LIST = []


def enter_input_data(surname, initial, location):
	BROWSER.get("https://www.whitepages.com.au/residential")
	BROWSER.delete_all_cookies()

	CONFIG_DATA['surname'] = surname
	CONFIG_DATA['initial'] = initial
	CONFIG_DATA['location'] = location

	surname_xpath = '//*[@id="residentialQueryField"]'
	initails_xpath = '//*[@id="residentialMiddleInitialField"]'
	location_xpath = '//*[@id="residentialLocationQueryField"]'
	search_btn_xpath = '//*[@id="residentialTab"]/div/div/div[2]/button'

	try:
		WebDriverWait(BROWSER, 10).until(EC.visibility_of_element_located((By.XPATH, surname_xpath)))
		surname_element = BROWSER.find_element_by_xpath(surname_xpath).send_keys(surname)
		time.sleep(1)

		initails_element = BROWSER.find_element_by_xpath(initails_xpath).send_keys(initial)
		time.sleep(1)

		location_element = BROWSER.find_element_by_xpath(location_xpath)
		length = len(location_element.get_attribute('value'))
		location_element.send_keys(length * Keys.BACKSPACE)
		location_element = BROWSER.find_element_by_xpath(location_xpath).send_keys(location)
		time.sleep(1)

		BROWSER.delete_all_cookies()
		time.sleep(0.5)
		search_btn_element = BROWSER.find_element_by_xpath(search_btn_xpath).click()
		time.sleep(1.5)

		get_all_PEOPLE_LIST()

	except Exception as err:
		cprint(f'      [x] Exception: {str(err)}', 'yellow', attrs=['bold'])
		input()


def get_all_PEOPLE_LIST():
	global PEOPLE_LIST
	more_available = True
	current_page = 1
	prev_total_count = 0
	current_total_count = 0

	cprint(f'\n   [+] Getting all available people in database', 'magenta', attrs=['bold'])

	while more_available:
		people_divs = BROWSER.find_elements_by_class_name('search-result-item-container')
		cprint(f'\n      [+] Getting all People link from Page # {current_page}', 'cyan', attrs=['bold'])
		for people_div in people_divs[3:]:
			link = people_div.find_element_by_tag_name('a').get_attribute('href')
			PEOPLE_LIST.append(link)
			# print(link)

		cprint(f'         [>] Total Number of people available so far: {len(PEOPLE_LIST)}', 'yellow', attrs=['bold'])
		current_total_count = len(PEOPLE_LIST)

		if prev_total_count == current_total_count:
			cprint(f'         [>] Seems we have fetched all people for given query.', 'yellow', attrs=['bold'])
			more_available = False
		else:
			cprint(f'         [>] Moving to next page.', 'yellow', attrs=['bold'])

			# # if len(PEOPLE_LIST) > 0 and len(PEOPLE_LIST) % 10 == 0:
			# more_available = check_next_page(len(PEOPLE_LIST))

			# if more_available:
			current_page += 1
			current_url = BROWSER.current_url

			if current_url.rsplit('&', 1)[-1].split('=')[0] == 'page':
				next_page_url = f'{BROWSER.current_url.rsplit("page=", 1)[0]}page={current_page}'
			else:
				next_page_url = f'{BROWSER.current_url}&page={current_page}'

			prev_total_count = current_total_count

			BROWSER.delete_all_cookies()
			BROWSER.get(next_page_url)
			# input()

	pull_person_data()


def pull_person_data():
	global PERSON_DATA
	global PERSON_COUNT

	count = 1
	cprint(f'\n   [+] Going To individual Person to get its data', 'magenta', attrs=['bold'])

	for person_link in PEOPLE_LIST:
		PERSON_COUNT += 1
		BROWSER.delete_all_cookies()
		BROWSER.get(person_link)

		try:
			person_name_element = WebDriverWait(BROWSER, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, 'contact-heading')))

			script_dict = debug_script_tag()
			if not script_dict['surname']:
				script_dict['surname'] = BROWSER.find_element_by_xpath('//*[@id="residentialQueryField"]').get_attribute('value').title()

			person_name = person_name_element.text.strip()

			honoraryTitle = person_name.split(" ")[0]
			if honoraryTitle not in ['Mr', 'Mrs', 'Mr.', 'Mrs.', "Miss"]:
				honoraryTitle = ''

			person_info = BROWSER.find_elements_by_class_name('contact-info')
			person_address = person_info[0].find_elements_by_tag_name('span')[-1].text.strip()
			person_contact = person_info[1].find_elements_by_tag_name('span')[-1].text.strip()

			address = BROWSER.find_element_by_class_name('sendSms_entryAddressPropertyAndLocality').get_attribute('innerHTML').split("</span>")
			property = address[0].replace("<span>", "").replace(",", "").strip()
			suburb = address[1].replace("<span>", "").strip()
			state = address[2].replace("<span>", "").strip()
			postcode = address[3].replace("<span>", "").strip()

			try:
				geo_code = BROWSER.find_element_by_class_name('wpMap-newSmallMapGetDirectionContainer').find_element_by_tag_name('a').get_attribute('href')
				latitude = geo_code.split('lat=')[-1].split('&')[0]
				longitude = geo_code.split('lon=')[-1].split('&')[0]
			except:
				latitude = None
				longitude = None

			cprint(f'      [{count}] Name: {person_name}', 'cyan', attrs=['bold'])
			cprint(f'          [>>] Property: {property}', 'yellow', attrs=['bold'])
			cprint(f'          [>>] Suburb: {suburb}', 'yellow', attrs=['bold'])
			cprint(f'          [>>] State: {state}', 'yellow', attrs=['bold'])
			cprint(f'          [>>] Zipcode: {postcode}', 'yellow', attrs=['bold'])
			cprint(f'          [>>] Contact: {person_contact}', 'yellow', attrs=['bold'])
			cprint(f'          [>>] Latitude: {latitude}', 'yellow', attrs=['bold'])
			cprint(f'          [>>] Longitude: {longitude}', 'yellow', attrs=['bold'])
			print()

			PERSON_DATA.append({
				'S.No.': PERSON_COUNT,
				'id': script_dict['id'] if 'id' in script_dict.keys() else None,
				'name': CONFIG_DATA['surname'],
				'location': CONFIG_DATA['location'],
				'initial': CONFIG_DATA['initial'],
				'count': count,
				'fullTitledName': person_name,
				'honoraryTitle': script_dict['honoraryTitle'] if 'honoraryTitle' in script_dict.keys() else None,
				'givenName': script_dict['givenName'] if 'givenName' in script_dict.keys() else None,
				'surname': script_dict['surname'] if 'surname' in script_dict.keys() else None,
				'geocode-lat': script_dict['latitude'] if 'latitude' in script_dict.keys() else None,
				'geocode-lon': script_dict['longitude'] if 'longitude' in script_dict.keys() else None,
				'property': script_dict['proprty'] if 'proprty' in script_dict.keys() else None,
				'suburb': script_dict['suburb'] if 'suburb' in script_dict.keys() else None,
				'state': script_dict['state'] if 'state' in script_dict.keys() else None,
				'postcode': script_dict['postcode'] if 'postcode' in script_dict.keys() else None,
				'locality': script_dict['locality'] if 'locality' in script_dict.keys() else None,
				'street': script_dict['street'] if 'street' in script_dict.keys() else None,
				'contact': person_contact
			})

			save_data_to_json()
			time.sleep(1.5)
			count += 1
		except Exception as err:
			cprint(f'    [X] Exception: {str(err)}', 'red', attrs=['bold'])


def save_data_to_json():
	with open('output.json', 'w') as data:
		json.dump(PERSON_DATA, data)
		create_csv()


def create_csv():
	 pd.DataFrame(PERSON_DATA).to_csv(CONFIG_DATA['output_file'], index=False)


def debug_script_tag():
	soup = BeautifulSoup(BROWSER.page_source, 'html.parser')
	scripts = soup.find_all('script', text = re.compile('__NUXT__'))

	for i in range(len(scripts)):
		script = str(scripts[i])
		script_dict = {}

		if '{streetVanity' in script:

			if 'id:"' in script:
				id = script.split('id:"')[-1].split('",')[0]
				# print("id: ", id)
			else:
				id = None

			if 'suburb:"' in script:
				suburb = script.split('suburb:"')[-1].split('",')[0]
				# print("suburb: ", suburb)
			else:
				suburb = None

			if 'state:"' in script:
				state = script.split('state:"')[-1].split('",')[0]
				# print("state: ", state)
			else:
				state = None

			if 'postcode:"' in script:
				postcode = script.split('postcode:"')[-1].split('",')[0]
				# print("postcode: ", postcode)
			else:
				postcode = None

			if 'property:"' in script:
				proprty = script.split('property:"')[-1].split('",')[0]
				# print("proprty: ", proprty)
			else:
				proprty = None

			if 'locality:"' in script:
				locality = script.split('locality:"')[-1].split('",')[0]
				# print("locality: ", locality)
			else:
				locality = None

			if 'street:"' in script:
				street = script.split('street:"')[-1].split('"}')[0]
				# print("street: ", street)
			else:
				street = None

			if '{lat:' in script:
				latitude = script.split('{lat:')[-1].split(',lon')[0]
				# print("latitude: ", latitude)
			else:
				latitude = None

			if ',lon:' in script:
				longitude = script.split(',lon:')[-1].split('},')[0]
				# print("longitude: ", longitude)
			else:
				longitude = None

			if 'honoraryTitle:"' in script:
				honoraryTitle = script.rsplit('honoraryTitle:"', 1)[-1].split('",')[0]
				# print("honoraryTitle: ", honoraryTitle)
			else:
				honoraryTitle = None

			if 'givenName:"' in script:
				givenName = script.split('givenName:"')[-1].split('",')[0]
				# print("givenName: ", givenName)
			else:
				givenName = None

			if 'surname:"' in script:
				surname = script.split('surname:"')[-1].split('"}')[0]
				# print("surname: ", surname)
			else:
				surname = None

			script_dict = {
				"id": id,
				"suburb": suburb,
				"state": state,
				"postcode": postcode,
				"proprty": proprty,
				"locality": locality,
				"street": street,
				"latitude": latitude,
				"longitude": longitude,
				"honoraryTitle": honoraryTitle,
				"givenName": givenName,
				"surname": surname
			}

			return script_dict
	return None


def check_next_page(total_people_fetched):
	next_page_div = 'search-pagination-container'
	try:
		next_page_container = WebDriverWait(BROWSER, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, next_page_div)))
		page_list = next_page_container.find_elements_by_tag_name('li')

		# for page in page_list:
		# 	print(page.text.strip(), end=', ')
		# print()

		counter = -1
		while True:
			try:
				# print(f'page_list[{counter}].text.strip() = {page_list[counter].text.strip()}')
				last_page = int(page_list[counter].text.strip())
				break
			except Exception as err:
				# input(f'Exception: {str(err)}')
				counter -= 1
				continue

		print(f'({total_people_fetched} // 10)+1 == {last_page} == {(total_people_fetched // 10)+1 == last_page}')

		if (total_people_fetched // 10)+1 == last_page:
			cprint(f'    [>] Seems we have fetched all people for given query.', 'yellow', attrs=['bold'])
			return False
		else:
			cprint(f'    [>] Moving to next page.', 'yellow', attrs=['bold'])
			return True

	except Exception as err:
		print(f' Exception: {str(err)})')
		cprint(f'    [>] Seems we have fetched all people for given query', 'yellow', attrs=['bold'])
		return False


# executing script only if its not imported
if __name__ == '__main__':
	init()
	intro_deco()
	initializer()

	# if not os.path.exists(PATH):
	# 	cprint(f'    [XX] Path {PATH} doesn\'t exists. Terminating Programm', 'red', attrs=['bold'])

	input_read = read_input_csv()

	if input_read:
		BROWSER = get_browser(headless=False)
		get_output_for_each_input()
		BROWSER.quit()
