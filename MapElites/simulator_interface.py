import share.moonboard_util as moonboard_util
from dataclasses import dataclass

@dataclass
class SimulationParams:
    dummy: int

def run_simulation(route: moonboard_util.MoonBoardRoute, params: SimulationParams) -> float:
    return 0.0
    