import os
import pathlib
import pandas as pd
import numpy as np
from share.moonboard_route import MoonBoardRoute
import MoonBoardRNN.BetaMove.preprocessing_helper as ph


def classify_and_reorganize_data_ga(route: MoonBoardRoute, feature_dict=None):
	if feature_dict is None:
		feature_dict = load_feature_dict()

	n_start = route.num_starting_holds()
	n_mid = route.num_mid_holds()
	n_hold = route.num_holds()
	start_sorted = sorted(route.start_holds, key=lambda h: h.row)
	mid_sorted = sorted(route.mid_holds, key=lambda h: h.row)
	end_sorted = sorted(route.end_holds, key=lambda h: h.row)
	all_holds = start_sorted + mid_sorted + end_sorted

	x_vectors = np.zeros((10, n_hold))
	for i, hold in enumerate(all_holds):
		x, y = hold.col, hold.row
		x_vectors[0:6, i] = feature_dict[(x, y)] # hand feature encoding
		x_vectors[6:8, i] = [x, y] # coordinate encoding
	x_vectors[8:, 0:n_start] = np.array([[1], [0]])
	x_vectors[8:, n_start + n_mid:] = np.array([[0], [1]])
	return x_vectors

def produce_sequence(hold_vectors):
	out = ph.produce_sequence(0, {0: hold_vectors}, 1)
	return out[0]

def route_to_x_vectors(route: MoonBoardRoute, feature_dict=None):
	route_id = route.get_id_str()
	data_dict = {route_id: classify_and_reorganize_data_ga(route, feature_dict)}
	beta = ph.produce_sequence(route_id, data_dict, printout=False)[0]
	x_vectors = beta_to_x_vectors(beta)
	return x_vectors

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

def beta_to_x_vectors(beta: ph.beta):
	"""
	Adopted from moveGeneratorForAllProblem
	"""
	numOfMoves = len(beta.handSequence) - 2
	movesInfoList = ph.moveGenerator(beta, string_mode = False)
	x_vectors = np.zeros((22, numOfMoves))
	
	for orderOfMove, moveInfoDict in enumerate(movesInfoList):   
		x_vectors[0:2, orderOfMove] = moveInfoDict['TargetHoldString'] 
		x_vectors[2, orderOfMove] = moveInfoDict['TargetHoldHand'] # only express once
		x_vectors[3, orderOfMove] = moveInfoDict['TargetHoldScore']
		x_vectors[4:6, orderOfMove] = moveInfoDict['RemainingHoldString']
		x_vectors[6, orderOfMove] = moveInfoDict['RemainingHoldScore']
		x_vectors[7:9, orderOfMove] = moveInfoDict['dxdyRtoT']
		x_vectors[9:11, orderOfMove] = moveInfoDict['MovingHoldString']
		x_vectors[11, orderOfMove] = moveInfoDict['MovingHoldScore']
		x_vectors[12:14, orderOfMove] = moveInfoDict['dxdyMtoT']
		x_vectors[14:21, orderOfMove] = moveInfoDict['FootPlacement']
		x_vectors[21, orderOfMove] = moveInfoDict['MoveSuccessRate']
	return x_vectors

def x_vectors_to_matrix(x_vectors):
	"""
	Pad with 0 vectors to get correct input shape
	"""
	matrix = np.zeros((12, 22))
	x_data = x_vectors.T
	matrix[0:x_data.shape[0], :] = x_data
	return matrix
