import pickle
import random
import matplotlib.pyplot as plt
from collections import defaultdict

precipitation = [] #precipitation in inches
training_data = [] #pairs - first element is date, second element is 0 (dry) or 1 (flowing)
test_data = []

with open("precipitation.p", "rb") as f:
    precipitation = pickle.load(f)

with open("blue_canyon/training_data.p", "rb") as f:
    training_data = pickle.load(f)

with open("blue_canyon/test_data.p", "rb") as f:
    test_data = pickle.load(f)

def get_failure_rate(evaporation_param, data_set):
    failure_count = 0
    for pt in data_set:
        level = 0
        start_index = pt[0] - 1000
        end_index = pt[0]
        for i in range(start_index, end_index):
            level += precipitation[i]
            level -= evaporation_param
            if level < 0:
                level = 0
        if (level <= 0 and pt[1] == 1) or (level > 0 and pt[1] == 0):
            failure_count += 1
    return float(failure_count) / len(data_set)

#training + cross-validation
#0.075 best evap rate
'''
results = {}
results = defaultdict(lambda: 0.0, results)

for j in range(0, 200):
    evaporation_param = j * 0.001
    failure_rate = get_failure_rate(evaporation_param, training_data)
    results[evaporation_param] = results[evaporation_param] + failure_rate

keys = results.keys()
values = results.values()
plt.xlabel("evaporation (inches/day)")
plt.ylabel("failure rate")
plt.plot(keys, values)
plt.show()
'''

#test
print(get_failure_rate(0.075, test_data))

