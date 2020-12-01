import csv
from csv import writer
import datetime

def appendList(file_name, flight_data): #adds the list containing the flight data in the CSV file
    with open(file_name, 'a+', newline='') as CSV_file:
        csv_writer = writer(CSV_file)
        csv_writer.writerow(flight_data)

def addCSVRows(CSV_file_name_to_add, CSV_file_name_to_create): #extracts lines from a CSV file and inserts them into another file
    with open(CSV_file_name_to_add) as CSV_file:
        csv_reader = csv.reader(CSV_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count != 0:
                appendList(CSV_file_name_to_create, row)
            line_count += 1

def main(complete_CSV, new_CSV, new_CSV_2):
    current_date = datetime.datetime.now().strftime('%d-%b-%Y')
    file_name = "arrivals_until_" + current_date + ".csv"

    with open(file_name, "w") as CSV_file:
        csv_output = csv.writer(CSV_file)
        csv_output.writerow(['Flight', 'Day', 'Flight From', 'Flight To', 'Aircraft', 'Flight Time', 'Scheduled Time Departure', 'Actual Time Departure', ' Scheduled Time Arrival', 'Status'])

    #estrae le righe dai file CSV e li unisce in un unico file CSV
    addCSVRows(complete_CSV, file_name)
    addCSVRows(new_CSV, file_name)
    addCSVRows(new_CSV_2, file_name)