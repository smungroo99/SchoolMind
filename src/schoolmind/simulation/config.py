from dataclasses import dataclass


@dataclass(frozen=True)
class SimulationConfig:
    width: int = 1000
    height: int = 700
    fish_count: int = 75
    fps: int = 60

    min_fish_speed: float = 70.0
    max_fish_speed: float = 120.0

    max_fish_acceleration: float = 500.0
    max_turn_rate: float = 5.0 # radians per second

    fish_radius: int = 5

    random_perturbation: bool = True