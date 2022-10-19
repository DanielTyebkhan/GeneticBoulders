import structs
from dataclasses import dataclass

@dataclass
class SimulationParams:
    dummy: int

def run_simulation(route: structs.MoonBoardRoute, params: SimulationParams) -> float:
    return 0.0
    