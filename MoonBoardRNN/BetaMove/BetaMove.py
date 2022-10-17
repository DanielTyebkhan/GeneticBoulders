"""
"""
from MoonBoardRNN.rnn_helpers import route_to_x_vectors
from structs import MoonboardRoute
import MoonBoardRNN.BetaMove.preprocessing_helper as ph

def find_route_beta(route: MoonboardRoute):
	route_id = route.get_id_str()
	data_dict = {route_id: route_to_x_vectors(route)}
	return ph.produce_sequence(route_id, data_dict)
		

