import ast
import datetime

def sortDict(unordered_dictionary): #order the dictionary with the flight code by key
    keys_sorted = sorted(unordered_dictionary.keys(), key=lambda x:x.lower())

    ordered_dictionary= {}
    for key in keys_sorted:
        ordered_dictionary.update({key: unordered_dictionary[key]})

    return ordered_dictionary

def addedMissingFlights(main_dictionary, missing_flights_dictionary):
	for k, v in missing_flights_dictionary.items():
		for i in v:
			if i not in [x for v in main_dictionary.values() for x in v]:
				main_dictionary.setdefault(k, [])
				main_dictionary[k].append(i)

	return main_dictionary

def dictionaryInTextFile(complete_dictionary):
	current_date = datetime.datetime.now().strftime('%Y_%m_%d')
	file_name = current_date + "_flight_codes.txt"
	
	with open(file_name, 'w') as f:
	    print(sortDict(complete_dictionary), file=f)

def main(main_dictionary, missing_flights_dictionary): #enters missing flight codes into the full dictionary
	with open(main_dictionary, "r") as data:
		main_dictionary = ast.literal_eval(data.read())

	with open(missing_flights_dictionary, "r") as data:
		missing_flights_dictionary = ast.literal_eval(data.read())

	complete_dictionary = addedMissingFlights(main_dictionary, missing_flights_dictionary)

	dictionaryInTextFile(complete_dictionary)
