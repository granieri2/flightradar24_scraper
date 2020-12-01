import os
import datetime
from time import sleep
from selenium import webdriver
from sys import exit
import shutil
import sys

sys.path.insert(0, 'Libs')
import credentials
import flight_code_extractor
import check_missing_codes
import arrivals_extractor_for_missing_codes
import arrivals_extractor_for_existing_codes
import add_missing_codes
import add_arrivals_extracted


def incognito(): #open browser in incognito mode
	firefox_profile = webdriver.FirefoxProfile()
	firefox_profile.set_preference("browser.privatebrowsing.autostart", True)
	return(firefox_profile)

def black_friday_popup_closure(b):
	b.implicitly_wait(5)
	if b.find_elements_by_xpath('//*[@id="subscription-promo-close"]'):
		b.find_element_by_xpath('//*[@id="subscription-promo-close"]').click()
	
def login(username, password, b): #login to the flightradar24 website
	b.implicitly_wait(5)
	b.find_element_by_xpath("//button[contains(@class, 'btn') and contains(@class, 'btn-blue')]").click()

	black_friday_popup_closure(b)

	b.implicitly_wait(5)
	b.find_element_by_xpath("//span[contains(@class, 'premium-menu-title') and contains(@class, 'premium-menu-title-login')]").click()

	b.implicitly_wait(5)
	b.find_element_by_xpath("//input[contains(@id, 'fr24_SignInEmail')]").send_keys(username)

	b.implicitly_wait(5)
	b.find_element_by_xpath("//input[contains(@id, 'fr24_SignInPassword')]").send_keys(password)

	b.implicitly_wait(5)
	b.find_element_by_xpath("//button[contains(@id, 'fr24_SignIn')]").click()

def checkBusinessAccount(b): #check if the business plan is active for data extraction
	b.get("https://www.flightradar24.com/")

	login(credentials.username, credentials.password, b)
	
	sleep(1)
	b.implicitly_wait(5)
	if b.find_elements_by_xpath("/html/body/div[4]/nav/div/ul/li/a/span[contains(text(), 'Business')]"):
		return True
	else:
		return False

def checkParameters(): #check the parameters entered in input
	if len(sys.argv) != 1 and len(sys.argv) != 3:

		print()
		print("\nWARNING!!! \n\n1) if it is the first use, do not pass any parameters to the program. \n\n2) if you have already used the program, pass the text file with the flight codes and the csv file with the arrival history to the program. \n")
		print()

		exit()

	elif len(sys.argv) > 1 and os.path.exists(sys.argv[1]) != True:

		print()
		print("WARNING!!!\n\nFirst parameter not present in the directory!")
		print()

		exit()

	elif len(sys.argv) > 2 and os.path.exists(sys.argv[2]) != True:

		print()
		print("WARNING!!!\n\nSecond parameter not present in the directory!")
		print()

		exit()

	elif len(sys.argv) == 3:
		if "flight_codes" not in sys.argv[1] and "arrivals_until" not in sys.argv[2]:

			print()
			print("WARNING!!!\n\nInsert the text file as the first parameter and the csv file as the second parameter!")
			print()

			exit()

def checkAccountStatus(): #the account status is checked
	b = webdriver.Firefox(firefox_profile=incognito())
	check_business_account = checkBusinessAccount(b)
	if check_business_account == False:
		print("Account with basic plan! The Business plan must be activated for the program to function correctly!")
		b.quit()
		sys.exit()
	elif check_business_account == True:
		print("Active Business Plan")
		b.quit()

def scrapingFirtTime():
	sleep(1)
	#Estrae il codice dei voli che ci sono stati il giorno precedente all'esecuzione del programma. I codici estratti vengono inseriti in un file di testo sotto forma di dictionary.
	extracted_flight_codes = flight_code_extractor.main(False)

	sleep(1)
	#Per i codici trovati vengono estratti gli arrivi in Italia dal 1° gennaio 2019 fino al giorno precedente all'esecuzione del programma. Gli arrivi estratti vengono inseriti in un file CSV.
	arrivals_extractor_for_missing_codes.main(extracted_flight_codes, False)

def scrapingSecondTime():
	dictionary = sys.argv[1]
	csv = sys.argv[2]

	sleep(1)
	#Estrae il codice dei voli che ci sono stati il giorno precedente all'esecuzione del programma.
	extracted_codes = flight_code_extractor.main(True)

	sleep(1)
	#Vengono confrontati i codici estratti con quelli gia presenti.
	missing_codes = check_missing_codes.main(dictionary, extracted_codes)

	sleep(1)
	#Per i codici non presenti vengono estratti gli arrivi in Italia dal 1° gennaio 2019 fino al giorno precedente all'esecuzione del programma.
	arrivals_for_missing_codes = arrivals_extractor_for_missing_codes.main(missing_codes, True)

	sleep(1)
	#Per i codici gia presenti vengono estratti gli arrivi che sono ci sono stati il giorno precedente all'esecuzione del programma.
	arrivals_for_existing_codes = arrivals_extractor_for_existing_codes.main(dictionary)



	sleep(1)
	#I codici mancanti vengono aggiunti al dictionary completo dei codici dei voli gia estratti.
	add_missing_codes.main(dictionary, missing_codes)

	sleep(1)
	#Gli arrivi estratti vengono aggiunti al CSV con gli arrivi gia estratti.
	add_arrivals_extracted.main(csv, arrivals_for_missing_codes, arrivals_for_existing_codes)



	shutil.move(csv, 'Previous days')
	print(csv + ": File moved!")

	shutil.move(dictionary, 'Previous days')
	print(dictionary + ": File moved!")

	os.remove(extracted_codes)
	print(extracted_codes + ": File Removed!")

	os.remove(missing_codes)
	print(missing_codes + ": File Removed!")

	os.remove(arrivals_for_missing_codes)
	print(arrivals_for_missing_codes + ": File Removed!")
	
	os.remove(arrivals_for_existing_codes)
	print(arrivals_for_existing_codes + ": File Removed!")

def main():
	startTime = datetime.datetime.now()

	checkParameters()

	checkAccountStatus()

	if len(sys.argv) == 1:
		scrapingFirtTime()

	elif len(sys.argv) == 3:
		scrapingSecondTime()

	print(datetime.datetime.now() - startTime)

main()
