#Flightradar24 Scraper
This is a Flightradar24 scraper written in Python.

It can fetch data on arrivals at Italian airports from 1 January 2019.

The goal of this project is to analyze the extracted data by comparing the differences between 2019 and 2020.

##Requirements
- Python v3.8.5 or greater
- Pip v20.0.2 or greater
- Selenium

##Quick Start
Make sure you have `Python 3.8.5` or above installed:

- `python3 --version`

Make sure you have `Pip 20.0.2` or above installed:

- `pip3 --version`

Install Selenium:

- `pip3 install selenium`

On Windows you might have to use `python` without the version (`3`) suffix.

To use the scraper on Windows download [geckodriver](https://chromedriver.chromium.org/) (if you use Google Chrome) or [chromedriver](https://github.com/mozilla/geckodriver/releases) (if you use Firefox).

**To use the scraper you must have activated the Business plan on Flightradar24.**<br />
**After activating the Business plan, enter the login data in `credentials.py`.**

##Usages
###First Usage
For the first use do not enter any parameters in input:

- `python3 flightradar24_scraper.py`

###More Usages
After the first use, two files will be generated which must be entered as input parameters for subsequent uses:

- `python3 flightradar24_scraper.py flight_codes_dd-mmm-aaaa.txt arrivals_until_dd-mmm-aaaa.csv`

##Advice
It is recommended to use the program at least once a day to collect the greatest number of flights and to have less extraction times.













