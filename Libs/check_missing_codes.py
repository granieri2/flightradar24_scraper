import ast
import datetime

def missingCodes(current_day_dictionary, previous_day_dictionary):
	missing_flights_dictionary = {}

	for k, v in current_day_dictionary.items():
		for i in v:
			if i not in [x for v in previous_day_dictionary.values() for x in v]:
				missing_flights_dictionary.setdefault(k, [])
				missing_flights_dictionary[k].append(i)	

	return missing_flights_dictionary

def dictionaryInTextFiles(missing_flights_dictionary):
	currente_date = datetime.datetime.now().strftime('%d-%b-%Y')
	file_name = 'missing_codes_' + currente_date + '.txt'

	with open(file_name, 'w') as f:
	    print(missing_flights_dictionary, file=f)

	return file_name

def main(main_dictionary, dictionary_to_compare): #compares the codes extracted today with those already present and extracts the missing ones
	with open(main_dictionary, "r") as data:
		previous_day_dictionary = ast.literal_eval(data.read())

	with open(dictionary_to_compare, "r") as data:
		current_day_dictionary = ast.literal_eval(data.read())

	missing_flights_dictionary = missingCodes(current_day_dictionary, previous_day_dictionary)

	file_name = dictionaryInTextFiles(missing_flights_dictionary)

	return file_name