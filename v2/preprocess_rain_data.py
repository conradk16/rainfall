#dumps a pickle file with an array of rain data with index 0 corresponding to Jan 1, 2011

import csv
import pickle

with open('precipitation.csv') as csv_file:
    data = csv.reader(csv_file, delimiter=',')
    precipitation = []
    next(data, None)

    for row in data:
        if row[3] == "":
            precipitation.append(0.0)
        else:
            precipitation.append(float(row[3]))
            
    with open("precipitation.p", "wb") as f:
        pickle.dump(precipitation, f)
