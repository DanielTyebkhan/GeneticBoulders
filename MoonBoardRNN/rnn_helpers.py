import numpy as np
from structs import MoonboardRoute

def route_to_x_vectors(route: MoonboardRoute):
    x_vectors = np.zeros((10, route.num_holds()))
    for i, hold in enumerate(route.holds):
        x, y = hold.row, hold.col
        x_vectors[0:6, i] = feature_dict[(x, y)] # hand feature encoding
        x_vectors[6:8, i] = [x, y] # coordinate encoding
    n_holds = route.num_holds()
    n_start = route.num_starting_holds()
    n_end = route.num_ending_holds()
    x_vectors[8:, 0:n_start] = np.array([[1], [0]])
    x_vectors[8:, n_holds - n_end:] = np.array([[0], [1]])
    return x_vectors