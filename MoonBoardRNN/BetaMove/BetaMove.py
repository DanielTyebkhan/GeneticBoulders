import os
import pathlib

import pandas as pd
import numpy as np

import MoonBoardRNN.BetaMove.preprocessing_helper as ph


def produce_sequence(hold_vectors):
	out = ph.produce_sequence(0, {0: hold_vectors}, 1)
	return out[0]

def normalization(matrix):
	tmax = matrix.shape[0]

	mu_x = 5.0428571
	sig_x = 3.079590
	mu_y = 9.8428571
	sig_y = 4.078289957
	mu_hand = 4.2428571
	sig_hand = 2.115829552
	mu_diff = 12.118308
	sig_diff = 11.495348196

	mu_vec = np.array([mu_x, mu_y, 0, mu_hand, mu_x, mu_y, mu_hand, 0, 0, mu_x, mu_y, mu_hand, 0, 0, 0, 0, 0, 0, 0, 0, 0, mu_diff])
	sig_vec = np.array([sig_x, sig_y, 1, sig_hand, sig_x, sig_y, sig_hand, sig_x, sig_y, sig_x, sig_y, sig_hand, sig_x, sig_y, 1, 1, 1, 1, 1, 1, 1, sig_diff])
    
	mask = np.zeros_like(matrix)
	mask[0:int(tmax), :] = 1
	normalized = np.copy(matrix)
	normalized -= mu_vec
	normalized /= sig_vec
	normalized *= mask

	return normalized

def load_feature_dict():
    dirname = pathlib.Path(__file__).parent
    file_path = os.path.join(dirname, 'HoldFeature2016.xlsx')
    features = pd.read_excel(file_path, dtype=str)
    feature_dict = {}
    for index in features.index:
        feature_item = features.loc[index]
        feature_dict[(int(feature_item['X_coord']), int(feature_item['Y_coord']))] = np.array(
			list(feature_item['Difficulties'])).astype(int)
    return feature_dict


def x_vectors_to_matrix(x_vectors):
	"""
	Pad with 0 vectors to get correct input shape
	"""
	matrix = np.zeros((12, 22))
	x_data = x_vectors.T
	matrix[0:x_data.shape[0], :] = x_data
	return matrix
