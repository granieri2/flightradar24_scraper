from selenium import webdriver
from csv import writer
import csv
import datetime
from time import sleep
import ast
import credentials
from selenium.webdriver.firefox.options import Options

def incognito(): #open browser in incognito mode
	firefox_profile = webdriver.FirefoxProfile()
	firefox_profile.set_preference("browser.privatebrowsing.autostart", True)
	return(firefox_profile)

def options():
	options = Options()
	options.headless = False

	return options
	
def login(username, password, b): #login to the flightradar24 website
	b.implicitly_wait(5)
	b.find_element_by_xpath("//button[contains(@class, 'btn') and contains(@class, 'btn-blue')]").click()
	
	b.implicitly_wait(5)
	b.find_element_by_xpath("//span[contains(@class, 'premium-menu-title') and contains(@class, 'premium-menu-title-login')]").click()

	b.implicitly_wait(5)
	b.find_element_by_xpath("//input[contains(@id, 'fr24_SignInEmail')]").send_keys(username)

	b.implicitly_wait(5)
	b.find_element_by_xpath("//input[contains(@id, 'fr24_SignInPassword')]").send_keys(password)

	b.implicitly_wait(5)
	b.find_element_by_xpath("//button[contains(@id, 'fr24_SignIn')]").click()

def loadFlights(b): #loads flights until January 1, 2019
	b.implicitly_wait(5)
	while b.find_elements_by_xpath("//button[contains(@id, 'btn-load-earlier-flights')]"):
		date_split = (b.find_element_by_xpath("//tr[contains(@class, 'data-row')][" + str(len(b.find_elements_by_xpath("//tr[contains(@class, 'data-row')]"))) + "]/td[3]").text).split(" ")
		b.implicitly_wait(5)
		if b.find_elements_by_xpath("//button[contains(@id, 'btn-load-earlier-flights')]") and int(date_split[2]) >= 2019:
			b.find_element_by_xpath("//button[contains(@id, 'btn-load-earlier-flights')]").click()
			sleep(2)
			if b.find_elements_by_xpath("//button[contains(@id, 'btn-load-earlier-flights') and contains(@class, 'loadButton') and contains(@class, 'loadEarlierFlights') and contains(@class, 'bottomMargin') and contains(@class, 'loading')]"):
				b.refresh()
		else:
			break

def monthNumber(month):
	switcher = {
		'Jan': 1,
		'Feb': 2,
		'Mar': 3,
		'Apr': 4,
		'May': 5,
		'Jun': 6,
		'Jul': 7,
		'Aug': 8,
		'Sep': 9,
		'Oct': 10,
		'Nov': 11,
		'Dec': 12
	}
	return switcher.get(month)

def currentDate():
	return datetime.datetime.now().strftime ('%Y %m %d')

def splitCurrentDate():
	return currentDate().split(" ")

def appendList(file_name, lista): #adds the list containing the flight data in the CSV file
    with open(file_name, 'a+', newline='') as CSV_file:
        csv_writer = writer(CSV_file)
        csv_writer.writerow(lista)

def numberMonthString(month):
    switcher = {
        'Jan': '01',
        'Feb': '02',
        'Mar': '03',
        'Apr': '04',
        'May': '05',
        'Jun': '06',
        'Jul': '07',
        'Aug': '08',
        'Sep': '09',
        'Oct': '10',
        'Nov': '11',
        'Dec': '12'
    }
    return switcher.get(month)

def appendRow(file_name, date_2, b, flight): #extracts flight data from January 1st 2019 to today
	for i in range(1, len(b.find_elements_by_xpath("//tr[contains(@class, 'data-row')]")) + 1):
		date_split = (b.find_element_by_xpath("//tr[contains(@class, 'data-row')][" + str(i) + "]/td[3]").text).split(" ")
		date_1 = datetime.date(int(date_split[2]), int(monthNumber(date_split[1])), int(date_split[0]))

		arrival = b.find_element_by_xpath("//tr[contains(@class, 'data-row')][" + str(i) + "]/td[5]")
		arrival_title = arrival.get_attribute('title')

		if date_1 < date_2 and "Italy" in arrival_title and int(date_split[2]) > 2018:
			flight_list = []
			flight_list.append(flight)
			data_flight = (b.find_element_by_xpath("//tr[contains(@class, 'data-row')][" + str(i) + "]/td[3]").text).split(" ") #date
			date_format = data_flight[2] + "-" + numberMonthString(data_flight[1]) + "-" + data_flight[0]
			flight_list.append(date_format)
			flight_list.append(b.find_element_by_xpath("//tr[contains(@class, 'data-row')][" + str(i) + "]/td[4]").text) #from
			flight_list.append(b.find_element_by_xpath("//tr[contains(@class, 'data-row')][" + str(i) + "]/td[5]").text) #to
			flight_list.append(b.find_element_by_xpath("//tr[contains(@class, 'data-row')][" + str(i) + "]/td[6]").text) #aircraft
			flight_list.append(b.find_element_by_xpath("//tr[contains(@class, 'data-row')][" + str(i) + "]/td[7]").text) #flight_time
			flight_list.append(b.find_element_by_xpath("//tr[contains(@class, 'data-row')][" + str(i) + "]/td[8]").text) #std
			flight_list.append(b.find_element_by_xpath("//tr[contains(@class, 'data-row')][" + str(i) + "]/td[9]").text) #atd
			flight_list.append(b.find_element_by_xpath("//tr[contains(@class, 'data-row')][" + str(i) + "]/td[10]").text) #sta
			flight_list.append(b.find_element_by_xpath("//tr[contains(@class, 'data-row')][" + str(i) + "]/td[12]").text) #status

			print(flight_list)
			appendList(file_name, flight_list) 

def checkUsage(check_usage):
	current_date = datetime.datetime.now().strftime('%d-%b-%Y')

	if check_usage == True: #controlla se non è il primo utilizzo
		file_name = "arrivals_for_missing_codes_" + current_date + ".csv"
	elif check_usage == False: #controlla se è il primo utilizzo
		file_name = "arrivals_until_" + current_date + ".csv"

	return file_name

def checkingBrowser(b):
	if b.find_elements_by_xpath('/html/body/table'): # controllo se si verifica il checking del browser per la sicurezza anti-ddos di CloudFlare
		print("Checking...")
		sleep(5)

def CSVCreation(dictionary_flights_today, file_name, b):
	with open(dictionary_flights_today, "r") as flights_dict:
		dictionary_flights_today = ast.literal_eval(flights_dict.read())

	with open(file_name, "w") as CSV_file:
		csv_output = csv.writer(CSV_file)
		csv_output.writerow(['Flight', 'Day', 'Flight From', 'Flight To', 'Aircraft', 'Flight Time', 'Scheduled Time Departure', 'Actual Time Departure', ' Scheduled Time Arrival', 'Status'])

	current_day_split = splitCurrentDate()
	current_day = datetime.date(int(current_day_split[0]), int(current_day_split[1]), int(current_day_split[2])) #formato data per confrontarla con quella su flightradar24

	sleep(2)
	for k, v in dictionary_flights_today.items(): 
		for flight in v:
			b.get("https://www.flightradar24.com/data/flights/" + flight)
			sleep(1)
			checkingBrowser(b)

			loadFlights(b)

			appendRow(file_name, current_day, b, flight)

def main(dictionary_flights_today, check_usage):
	b = webdriver.Firefox(options=options(), firefox_profile=incognito())

	b.get("https://www.flightradar24.com/")

	login(credentials.username, credentials.password, b)

	file_name = checkUsage(check_usage)

	CSVCreation(dictionary_flights_today, file_name, b)

	b.quit()

	return file_name

