#dumps training/validation, and test from water_data

import pickle
import random

#returns a pair: a list of flowing data points, and a list of not flowing data points
def get_flowing_and_not_flowing(water_data):
    flowing = []
    not_flowing = []
    for pt in water_data:
        if (pt[1] == 1):
            flowing.append(pt)
        else:
            not_flowing.append(pt)
    return (flowing, not_flowing)


streams = []
with open('streams.txt', 'r') as f:
    streams = f.read().splitlines()

for stream in streams:
    water_data = [] #pairs - first element is date, second element is 0 (dry) or 1 (flowing)

    with open(stream + '/' + 'water_data.p', "rb") as f:
        water_data = pickle.load(f)

    #sort into flowing and not flowing
    flowing, not_flowing = get_flowing_and_not_flowing(water_data)

    #add test and training from flowing points
    random.shuffle(flowing)

    test_start_index = len(flowing) - int(len(flowing)/3)

    training_data_points = flowing[0:test_start_index] 
    test_data_points = flowing[test_start_index:len(flowing)]

    #add test and training from not_flowing points
    random.shuffle(not_flowing)

    test_start_index = len(not_flowing) - int(len(not_flowing)/3)

    training_data_points.extend(not_flowing[0:test_start_index])
    test_data_points.extend(not_flowing[test_start_index:len(not_flowing)])
    

    with open(stream + '/' + 'training_data.p', "wb") as f:
        pickle.dump(training_data_points, f)

    with open(stream + '/' + 'test_data.p', "wb") as f:
        pickle.dump(test_data_points, f)
