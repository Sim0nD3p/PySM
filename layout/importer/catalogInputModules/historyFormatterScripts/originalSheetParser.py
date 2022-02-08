import csv

print('originalSheetParser for orders')

file_path = 'C:/Users/simon/Documents/Techno-Fab/PySM/PySM/layout/importer/catalogInputModules/historyFormatterScripts/achats.csv'

with open(file_path, 'r') as csv_file:
    reader = csv.reader(csv_file)
    for row in reader:
        if row[1]:
            date = row[1]
        
