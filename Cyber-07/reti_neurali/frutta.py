import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from collections import Counter


np.random.seed(42)

def distance(instance1, instance2):
    """ Calculates the Eucledian distance between two instances""" 
    return np.linalg.norm(np.subtract(instance1, instance2))

def get_neighbors(training_set, 
                  labels, 
                  test_instance, 
                  k, 
                  distance):
    """
    get_neighors calculates a list of the k nearest neighbors
    of an instance 'test_instance'.
    The function returns a list of k 3-tuples.
    Each 3-tuples consists of (index, dist, label)
    where 
    index    is the index from the training_set, 
    dist     is the distance between the test_instance and the 
             instance training_set[index]
    distance is a reference to a function used to calculate the 
             distances
    """
    distances = []
    for index in range(len(training_set)):
        dist = distance(test_instance, training_set[index])
        distances.append((training_set[index], dist, labels[index]))
    distances.sort(key=lambda x: x[1])
    neighbors = distances[:k]
    return neighbors


def vote_harmonic_weights(neighbors, all_results=True):
    class_counter = Counter()
    number_of_neighbors = len(neighbors)
    for index in range(number_of_neighbors):
        class_counter[neighbors[index][2]] += 1/(index+1)
    labels, votes = zip(*class_counter.most_common())
    #print(labels, votes)
    winner = class_counter.most_common(1)[0][0]
    votes4winner = class_counter.most_common(1)[0][1]
    if all_results:
        total = sum(class_counter.values(), 0.0)
        for key in class_counter:
             class_counter[key] /= total
        return winner, class_counter.most_common()
    else:
        return winner, votes4winner / sum(votes)

def create_features(number_samples, *min_max_features):
    """ Creates an array with number_samples rows and len(min_max_features) columns """
    features = []
    for min_val, max_val,rounding in min_max_features:
        features.append(np.random.uniform(min_val, max_val, number_samples).round(rounding))
    result = np.column_stack(features)
    return result

num_apples, num_mangos, num_lemons = 150, 150, 150
sweetness = (10, 18, 0)
acidity = 3.4, 4, 2
weight = 140.0, 250.0, 0
apples = create_features(num_apples, sweetness, acidity, weight)
print(apples[:20]) # The first 20 fruits

sweetness = (6, 14, 0)
acidity = 3.6, 6, 1       # should be between 5.8 and 6
weight = 100.0, 300.0, 0
mangos = create_features(num_mangos, sweetness, acidity, weight)

sweetness = (6, 12, 0)
acidity = 2.0, 2.6, 1
weight = 130, 170, 0
lemons = create_features(num_lemons, sweetness, acidity, weight)

# Combine the data and create labels
X = np.vstack((apples, mangos, lemons))
y = np.array(['Apple'] * num_apples + ['Mango'] * num_mangos + ['Lemon'] * num_lemons)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

import pandas as pd

# Define the DataFrame
df = pd.DataFrame(X, columns=['Sweetness', 'Acidity', 'Weight'])
df['Fruit'] = y

# Write DataFrame to CSV file
df.to_csv('data/fruits_data.csv', index=False)

n_test_samples = len(X_test)
    
for i in range(20):
    neighbors = get_neighbors(X_train, 
                              y_train, 
                              X_test[i], 
                              6, 
                              distance=distance)

    print("index: ", i, 
          ", result of vote: ", 
          vote_harmonic_weights(neighbors, all_results=True))
    