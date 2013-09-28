from similarity.distance.pearson_distance import PearsonDistance
import numpy as np

print PearsonDistance().distance(np.array([[1, 2, 4]]), np.array([[1, 2, 3]]))