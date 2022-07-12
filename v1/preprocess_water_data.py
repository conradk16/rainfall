#dumps a pickle file with an array of pairs (date_index, <0,1>), where date_index corresponds to the number of days since Jan 1, 2011, and 0 represents dry while 1 represents flowing.

import csv
import pickle
from datetime import date

date_zero = date(2011, 1, 1)

with open('forbush/forbush.csv') as csv_file:
    data = csv.reader(csv_file, delimiter=',')
    next(data, None)
    water_data = []

    for row in data:
        flowing = 0
        if row[2] == "Flowing":
            flowing = 1

        date_string = row[0]
        elements = date_string.split('/')
        current_date = date(int("20" + elements[2]), int(elements[0]), int(elements[1]))
        delta = current_date - date_zero
        days = delta.days
        
        water_data.append((days, flowing))

    with open("forbush/water_data.p", "wb") as f:
        pickle.dump(water_data, f)
