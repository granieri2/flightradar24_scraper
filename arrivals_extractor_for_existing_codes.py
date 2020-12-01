from selenium import webdriver
from csv import writer
from time import sleep
import csv
import datetime
import ast
from selenium.webdriver.firefox.options import Options

def incognito(): #open browser in incognito mode
	firefox_profile = webdriver.FirefoxProfile()
	firefox_profile.set_preference("browser.privatebrowsing.autostart", True)
	return(firefox_profile)

def options():
	options = Options()
	options.headless = False

	return options

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

def previousDay(): #calculates the date of the previous day
	previous_day = datetime.datetime.today() - datetime.timedelta(days=1)
	return previous_day.strftime ('%Y %m %d')

def splitPreviousDay():
	return previousDay().split(" ")

def appendList(file_name, flight_data): #adds the list containing the flight data in the CSV file
    with open(file_name, 'a+', newline='') as CSV_file:
        csv_writer = writer(CSV_file)
        csv_writer.writerow(flight_data)

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

def appendRow(file_name, date_2, b, flight): #extracts flight data from the previous day
	for i in range(1, len(b.find_elements_by_xpath("//tr[contains(@class, 'data-row')]")) + 1):
		date_split = (b.find_element_by_xpath("//tr[contains(@class, 'data-row')][" + str(i) + "]/td[3]").text).split(" ")
		date_1 = datetime.date(int(date_split[2]), int(monthNumber(date_split[1])), int(date_split[0]))

		arrival = b.find_element_by_xpath("//tr[contains(@class, 'data-row')][" + str(i) + "]/td[5]")
		title_arrival = arrival.get_attribute('title')

		if date_1 == date_2 and "Italy" in title_arrival:
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

def checkingBrowser(b):
	if b.find_elements_by_xpath('/html/body/table'): # controllo se si verifica il checking del browser per la sicurezza anti-ddos di CloudFlare
		print("Checking...")
		sleep(5)

def CSVCreation(dict_flights, b):
	current_date = datetime.datetime.now().strftime('%d-%b-%Y')
	file_name = "arrivals_for_existing_codes_"+current_date+".csv"

	with open(file_name, "w") as f_output:
		CSV_output = csv.writer(f_output)
		CSV_output.writerow(['Flight', 'Day', 'Flight From', 'Flight To', 'Aircraft', 'Flight Time', 'Scheduled Time Departure', 'Actual Time Departure', ' Scheduled Time Arrival', 'Status'])

	previous_day_split = splitPreviousDay()
	year = previous_day_split[0]
	month = previous_day_split[1]
	day = previous_day_split[2]
	previous_day = datetime.date(int(year), int(month), int(day)) #formato data per confrontarla con quella su flightradar24

	with open(dict_flights, "r") as diz_voli:
		dict_flights = ast.literal_eval(diz_voli.read())

	for k, v in dict_flights.items(): 
		for flight in v:
			b.get("https://www.flightradar24.com/data/flights/" + flight)
			sleep(1)
			checkingBrowser(b)
			sleep(1)

			appendRow(file_name, previous_day, b, flight)
			sleep(1)

	return file_name

def main(dict_flights):
	b = webdriver.Firefox(options=options(), firefox_profile=incognito())
	#b = webdriver.Firefox(options=options, firefox_profile=incognito(), executable_path=r'C:\Users\jj\Documents\ubuntuVB\ubuntu\Documenti\tirocinio\scraping flightradar\geckodriver.exe')

	file_name = CSVCreation(dict_flights, b)

	b.quit()

	return file_name
