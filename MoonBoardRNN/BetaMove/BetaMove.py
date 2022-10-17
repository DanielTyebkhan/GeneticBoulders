"""
"""
from structs import MoonboardRoute
import preprocessing_helper as ph

def find_route_beta(route: MoonboardRoute):
	return ph.produce_sequence(route.Id, route.to_dict)
		

