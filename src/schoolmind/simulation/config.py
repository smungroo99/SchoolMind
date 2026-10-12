from dataclasses import dataclass


@dataclass(frozen=True)
class SimulationConfig:
    width: int = 1000
    height: int = 700
    fish_count: int = 75
    fps: int = 60

    # Fish movement
    fish_speed: float = 225.0
    max_fish_acceleration: float = 500.0
    max_turn_rate: float = 5.0
    fish_radius: int = 5
    random_perturbation: bool = True

    # Aquarium boundaries
    fish_boundary_margin: float = 100.0
    predator_boundary_margin: float = 0.0

    # Boids
    neighbor_radius: float = 100.0
    separation_radius: float = 25.0
    separation_weight: float = 1.5
    alignment_weight: float = 1.0
    cohesion_weight: float = 0.8

    # Predators
    predator_count: int = 1
    predator_max_speed: float = 170.0
    predator_max_acceleration: float = 400.0
    predator_detection_range: float = 250.0
    predator_capture_radius: float = 12.0
    predator_capture_cooldown: float = 1.5
    predator_avoidance_weight: float = 3.0
    predator_separation_radius: float = 50.0
    predator_separation_weight: float = 5.0

    # Social predation risk
    predation_baseline_hazard: float = 4.0
    predation_social_radius: float = 100.0

    predation_exposure_strength: float = 1.5
    predation_exposure_saturation: float = 2.0

    predation_dilution_strength: float = 0.35
    predation_dilution_saturation: float = 4.0

    predation_confusion_strength: float = 0.35
    predation_confusion_saturation: float = 4.0
    predation_confusion_distance_scale: float = 50.0

    predation_crowding_strength: float = 0.75
    predation_crowding_distance: float = 15.0
    predation_crowding_scale: float = 5.0

    # Predator behavior
    predator_coordination_mode: str = "independent"

    # Options:
    # "coordinated", "independent"