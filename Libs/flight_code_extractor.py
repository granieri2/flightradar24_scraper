from selenium import webdriver
import datetime 
import calendar 
from time import sleep
from selenium.webdriver.firefox.options import Options

def incognito(): #open browser in incognito mode
	firefox_profile = webdriver.FirefoxProfile()
	firefox_profile.set_preference("browser.privatebrowsing.autostart", True)
	return firefox_profile

def options():
	options = Options()
	options.headless = False

	return options

def findDay(date): #find day of the week
    day = datetime.datetime.strptime(date, '%d %m %Y').weekday() 
    return calendar.day_name[day]

def previousDay(): #calculates the previous day
	previous_day = datetime.datetime.today() - datetime.timedelta(days=1)
	formatting_previous_day_1 = previous_day.strftime ('%d %m %Y')
	formatting_previous_day_2 = previous_day.strftime ('%b %d')
	previous_day = findDay(formatting_previous_day_1) + ", " + str(formatting_previous_day_2)
	return(previous_day)

def checkingBrowser(b):
	if b.find_elements_by_xpath('/html/body/table'): # controllo se si verifica il checking del browser per la sicurezza anti-ddos di CloudFlare
		print("Checking...")
		sleep(5)

def flightCodesExtraction(airport_IATA_codes, b):
	flights = {}

	for code in airport_IATA_codes:
		b.get("https://www.flightradar24.com/data/airports/" + code + "/arrivals")
		
		sleep(1)
		checkingBrowser(b)
			
		flights.setdefault(code, [])

		b.implicitly_wait(2)
		if b.find_elements_by_xpath("//tr[contains(@class, 'row-date-separator') and contains(@class, 'hidden-xs') and contains(@class, 'hidden-sm')]"):        
				b.find_element_by_xpath("//button[contains(@class, 'btn') and contains(@class, 'btn-table-action') and contains(@class, 'btn-flights-load')]").click() #click sul button per visualizzare i voli del giorno precedente
				sleep(2)

				b.implicitly_wait(2)
				for i in range(1, len(b.find_elements_by_xpath("//tr[contains(@class, 'hidden-xs') and contains(@class, 'hidden-sm') and contains(@class, 'ng-scope') and contains(@data-date, '" + previousDay() + "')]")) + 1): #vengono estratti tutti i codici dei voli del giorno precedente
					if b.find_elements_by_xpath("//tr[contains(@class, 'hidden-xs') and contains(@class, 'hidden-sm') and contains(@class, 'ng-scope') and contains(@data-date, '" + previousDay() + "')][" + str(i) + "]/td[2]/a[2]"):
						if b.find_element_by_xpath("//tr[contains(@class, 'hidden-xs') and contains(@class, 'hidden-sm') and contains(@class, 'ng-scope') and contains(@data-date, '" + previousDay() + "')][" + str(i) + "]/td[2]/a[2]").text not in [x for v in flights.values() for x in v]:
							flights[code].append(b.find_element_by_xpath("//tr[contains(@class, 'hidden-xs') and contains(@class, 'hidden-sm') and contains(@class, 'ng-scope') and contains(@data-date, '" + previousDay() + "')][" + str(i) + "]/td[2]/a[2]").text)
					else:
						if b.find_element_by_xpath("//tr[contains(@class, 'hidden-xs') and contains(@class, 'hidden-sm') and contains(@class, 'ng-scope') and contains(@data-date, '" + previousDay() + "')][" + str(i) + "]/td[2]/a[1]").text not in [x for v in flights.values() for x in v]:
							flights[code].append(b.find_element_by_xpath("//tr[contains(@class, 'hidden-xs') and contains(@class, 'hidden-sm') and contains(@class, 'ng-scope') and contains(@data-date, '" + previousDay() + "')][" + str(i) + "]/td[2]/a[1]").text)

	return flights

def checkUsage(check_usage, flights):
	current_date = datetime.datetime.now().strftime('%d-%b-%Y')

	if check_usage == True: #controlla se non è il primo utilizzo
		file_name = 'extracted_codes_' + current_date + '.txt'
		with open(file_name, 'w') as f:
			print(flights, file=f)
	elif check_usage == False: #controlla se è il primo utilizzo
		file_name = 'flight_codes_' + current_date + '.txt'
		with open(file_name, 'w') as f:
			print(flights, file=f)
	
	return file_name

def main(check_usage):
	b = webdriver.Firefox(options=options(), firefox_profile=incognito())
	b.get("https://www.flightradar24.com/data/airports/italy")

	airport_IATA_codes = [link.get_attribute('data-iata') for link in b.find_elements_by_xpath("//tbody/tr/td[2]/a")] #estrazione link di ogni aeroporto

	flights = flightCodesExtraction(airport_IATA_codes, b)

	file_name = checkUsage(check_usage, flights)
  
	b.quit()

	return file_name
