#dumps training/validation, and test from water_data

import pickle
import random

water_data = [] #pairs - first element is date, second element is 0 (dry) or 1 (flowing)

with open("forbush/water_data.p", "rb") as f:
    water_data = pickle.load(f)

random.shuffle(water_data)

test_start_index = len(water_data) - int(len(water_data)/5)

training_data_points = water_data[0:test_start_index] 
test_data_points = water_data[test_start_index:len(water_data)]

with open("forbush/training_data.p", "wb") as f:
    pickle.dump(training_data_points, f)

with open("forbush/test_data.p", "wb") as f:
    pickle.dump(test_data_points, f)


