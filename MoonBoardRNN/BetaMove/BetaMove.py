import os
import pathlib
import pandas as pd
import numpy as np
from structs import MoonBoardRoute
import MoonBoardRNN.BetaMove.preprocessing_helper as ph

def route_to_x_vectors(route: MoonBoardRoute):
	route_id = route.get_id_str()
	data_dict = {route_id: route_to_hold_vectors(route)}
	beta = ph.produce_sequence(route_id, data_dict, printout=True)[0]
	x_vectors = beta_to_x_vectors(beta)
	return x_vectors

def __load_feature_dict():
    dirname = pathlib.Path(__file__).parent
    file_path = os.path.join(dirname, 'HoldFeature2016.xlsx')
    features = pd.read_excel(file_path, dtype=str)
    feature_dict = {}
    for index in features.index:
        feature_item = features.loc[index]
        feature_dict[(int(feature_item['X_coord']), int(feature_item['Y_coord']))] = np.array(
			list(feature_item['Difficulties'])).astype(int)
    return feature_dict

def route_to_hold_vectors(route: MoonBoardRoute):
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