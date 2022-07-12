import pickle
import random
import matplotlib.pyplot as plt
from collections import defaultdict
import sys

precipitation = [] #precipitation in inches
training_data = [] #pairs - first element is date, second element is 0 (dry) or 1 (flowing)
test_data = []

#args
if len(sys.argv) < 3:
    sys.exit('Usage: <stream> <learn/test/predict> [evap_rate]')
stream = sys.argv[1]
mode = sys.argv[2]
if mode == "test" or mode == "predict":
    if len(sys.argv) != 4:
        sys.exit('Usage: <stream> <learn/test> [evap_rate]')
    evap_rate = float(sys.argv[3])

with open("precipitation.p", "rb") as f:
    precipitation = pickle.load(f)

with open(stream + '/' + 'training_data.p', "rb") as f:
    training_data = pickle.load(f)

with open(stream + '/' + 'test_data.p', "rb") as f:
    test_data = pickle.load(f)

#returns a pair: (false positive rate, false negative rate)
def get_failure_rate(evaporation_param, data_set):
    false_positive_count = 0
    false_negative_count = 0
    positive_count = 0
    negative_count = 0
    for pt in data_set:
        level = 0
        start_index = pt[0] - 1000
        end_index = pt[0]
        for i in range(start_index, end_index):
            level += precipitation[i]
            level -= evaporation_param
            if level < 0:
                level = 0
        if pt[1] == 1:
            positive_count += 1
            if level == 0:
                false_negative_count += 1
        elif pt[1] == 0:
            negative_count += 1
            if level > 0:
                false_positive_count += 1
    return (float(false_positive_count) / negative_count, float(false_negative_count) / positive_count)

#returns True for water, false o.w.
def predict(evaporation_param):
    level = 0
    end_index = len(precipitation) - 1
    start_index = end_index - 1000
    for i in range(start_index, end_index):
        level += precipitation[i]
        level -= evaporation_param
        if level < 0:
            level = 0
    return level > 0

if mode == "learn":
    #training + cross-validation
    results = {} #evap_rates map to failure pair
    results = defaultdict(lambda: (0.0,0.0), results)

    for j in range(0, 500):
        evaporation_param = j * 0.001
        false_positive_rate, false_negative_rate = get_failure_rate(evaporation_param, training_data)
        results[evaporation_param] = (false_positive_rate, false_negative_rate)

    evap_rates = results.keys()
    false_positives, false_negatives = zip(*results.values())
    plt.xlabel("evaporation (inches/day)")
    #plt.ylabel("failure rate")
    plt.plot(evap_rates, false_positives, label = "false_positives")
    plt.plot(evap_rates, false_negatives, label = "false_negatives")
    plt.legend()
    plt.show()
elif mode == "test":
    #test
    print(get_failure_rate(evap_rate, test_data))
elif mode == "predict":
    print(predict(evap_rate))

