import os
import pathlib
import pandas as pd
import numpy as np
from structs import MoonboardRoute

def __load_feature_dict():
    dirname = pathlib.Path(__file__).parent
    file_path = os.path.join(dirname, 'BetaMove', 'HoldFeature2016.xlsx')
    features = pd.read_excel(file_path, dtype=str)
    feature_dict = {}
    for index in features.index:
        feature_item = features.loc[index]
        feature_dict[(int(feature_item['X_coord']), int(feature_item['Y_coord']))] = np.array(
            list(feature_item['Difficulties'])).astype(int)
    return feature_dict

def route_to_x_vectors(route: MoonboardRoute):
    x_vectors = np.zeros((10, route.num_holds()))
    feature_dict = __load_feature_dict()
    for i, hold in enumerate(route.holds):
        x, y = hold.col, hold.row
        x_vectors[0:6, i] = feature_dict[(x, y)] # hand feature encoding
        x_vectors[6:8, i] = [x, y] # coordinate encoding
    n_holds = route.num_holds()
    n_start = route.num_starting_holds()
    n_end = route.num_ending_holds()
    x_vectors[8:, 0:n_start] = np.array([[1], [0]])
    x_vectors[8:, n_holds - n_end:] = np.array([[0], [1]])
    return x_vectors