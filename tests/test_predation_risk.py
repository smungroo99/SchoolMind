
import pygame

from schoolmind.simulation.config import SimulationConfig
from schoolmind.simulation.fish import Fish
from schoolmind.simulation.predator import Predator
from schoolmind.simulation.predation_risk import (
    calculate_capture_hazard,
    calculate_capture_probability,
    calculate_capture_risk,
    calculate_cohesion,
    calculate_confusion,
    calculate_crowding,
    calculate_dilution,
    calculate_dispersion,
    calculate_exposure,
)
from schoolmind.simulation.world import World


def make_fish(
    fish_id: int,
    position: tuple[float, float],
    velocity: tuple[float, float],
) -> Fish:
    fish = Fish(
        fish_id=fish_id,
        position=pygame.Vector2(position),
        target_speed=225.0,
        max_speed=225.0,
        max_acceleration=500.0,
        max_turn_rate=5.0,
        world_width=1000,
        world_height=700,
        radius=5,
        boundary_margin=100.0,
        random_perturbation=False,
    )
    fish.velocity = pygame.Vector2(velocity)
    return fish


def make_predator(
    position: tuple[float, float],
) -> Predator:
    return Predator(
        predator_id=0,
        position=pygame.Vector2(position),
        max_speed=170.0,
        max_acceleration=400.0,
        detection_range=250.0,
        capture_radius=12.0,
        capture_cooldown=1.5,
        world_width=1000,
        world_height=700,
        boundary_margin=0.0,
    )


def test_isolated_fish_has_maximum_exposure() -> None:
    target = make_fish(0, (500.0, 350.0), (100.0, 0.0))
    predator = make_predator((512.0, 350.0))

    exposure = calculate_exposure(
        target=target,
        predator=predator,
        neighbors=[],
        exposure_radius=100.0,
        exposure_saturation=2.0,
    )

    assert exposure == 1.0


def test_front_neighbor_reduces_exposure() -> None:
    target = make_fish(0, (500.0, 350.0), (100.0, 0.0))
    predator = make_predator((550.0, 350.0))
    front_neighbor = make_fish(1, (525.0, 350.0), (100.0, 0.0))

    exposure = calculate_exposure(
        target=target,
        predator=predator,
        neighbors=[front_neighbor],
        exposure_radius=100.0,
        exposure_saturation=2.0,
    )

    assert exposure < 1.0


def test_neighbor_behind_target_does_not_shield_predator_facing_side() -> None:
    target = make_fish(0, (500.0, 350.0), (100.0, 0.0))
    predator = make_predator((550.0, 350.0))
    rear_neighbor = make_fish(1, (475.0, 350.0), (100.0, 0.0))

    exposure = calculate_exposure(
        target=target,
        predator=predator,
        neighbors=[rear_neighbor],
        exposure_radius=100.0,
        exposure_saturation=2.0,
    )

    assert exposure == 1.0


def test_neighbor_behind_predator_does_not_shield_target() -> None:
    target = make_fish(0, (525.0, 350.0), (100.0, 0.0))
    predator = make_predator((500.0, 350.0))
    neighbor = make_fish(1, (475.0, 350.0), (100.0, 0.0))

    exposure_without_neighbor = calculate_exposure(
        target=target,
        predator=predator,
        neighbors=[],
        exposure_radius=100.0,
        exposure_saturation=2.0,
    )
    exposure_with_neighbor = calculate_exposure(
        target=target,
        predator=predator,
        neighbors=[neighbor],
        exposure_radius=100.0,
        exposure_saturation=2.0,
    )

    assert exposure_without_neighbor == 1.0
    assert exposure_with_neighbor == exposure_without_neighbor


def test_neighbor_off_predator_target_line_does_not_shield() -> None:
    target = make_fish(0, (500.0, 350.0), (100.0, 0.0))
    predator = make_predator((550.0, 350.0))
    neighbor = make_fish(1, (525.0, 365.0), (100.0, 0.0))

    exposure = calculate_exposure(
        target=target,
        predator=predator,
        neighbors=[neighbor],
        exposure_radius=100.0,
        exposure_saturation=2.0,
    )

    assert exposure == 1.0


def test_dispersion_increases_with_neighbor_distance() -> None:
    close_neighbors = calculate_dispersion(
        neighbor_count=2,
        mean_neighbor_distance=20.0,
        social_radius=100.0,
    )
    distant_neighbors = calculate_dispersion(
        neighbor_count=2,
        mean_neighbor_distance=80.0,
        social_radius=100.0,
    )

    assert close_neighbors == 0.2
    assert distant_neighbors == 0.8
    assert distant_neighbors > close_neighbors


def test_isolated_fish_has_maximum_dispersion_score() -> None:
    assert calculate_dispersion(
        neighbor_count=0,
        mean_neighbor_distance=None,
        social_radius=100.0,
    ) == 1.0


def test_cohesion_risk_increases_with_distance_from_group_center() -> None:
    near_center = calculate_cohesion(
        neighbor_count=2,
        cohesion_distance=10.0,
        social_radius=100.0,
    )
    far_from_center = calculate_cohesion(
        neighbor_count=2,
        cohesion_distance=60.0,
        social_radius=100.0,
    )

    assert near_center == 0.1
    assert far_from_center == 0.6
    assert far_from_center > near_center


def test_isolated_fish_has_maximum_cohesion_risk_score() -> None:
    assert calculate_cohesion(
        neighbor_count=0,
        cohesion_distance=None,
        social_radius=100.0,
    ) == 1.0


def test_dilution_increases_with_neighbor_count() -> None:
    no_dilution = calculate_dilution(0, 4.0)
    some_dilution = calculate_dilution(2, 4.0)
    more_dilution = calculate_dilution(10, 4.0)

    assert no_dilution == 0.0
    assert 0.0 < some_dilution < more_dilution
    assert more_dilution < 1.0


def test_aligned_neighbors_create_more_confusion() -> None:
    target = make_fish(0, (500.0, 350.0), (100.0, 0.0))
    predator = make_predator((550.0, 350.0))
    aligned_neighbor = make_fish(1, (500.0, 360.0), (100.0, 0.0))
    orthogonal_neighbor = make_fish(1, (500.0, 360.0), (0.0, 100.0))

    aligned_confusion = calculate_confusion(
        target=target,
        predator=predator,
        neighbors=[aligned_neighbor],
        distance_scale=50.0,
        saturation=4.0,
    )
    orthogonal_confusion = calculate_confusion(
        target=target,
        predator=predator,
        neighbors=[orthogonal_neighbor],
        distance_scale=50.0,
        saturation=4.0,
    )

    assert aligned_confusion > orthogonal_confusion
    assert aligned_confusion > 0.0


def test_crowding_increases_as_nearest_neighbor_gets_closer() -> None:
    spread_out = calculate_crowding(100.0, 15.0, 5.0)
    moderate = calculate_crowding(20.0, 15.0, 5.0)
    crowded = calculate_crowding(5.0, 15.0, 5.0)

    assert spread_out < moderate < crowded


def test_capture_probability_increases_with_hazard() -> None:
    low_probability = calculate_capture_probability(
        capture_hazard=1.0,
        dt=1.0 / 60.0,
    )
    high_probability = calculate_capture_probability(
        capture_hazard=5.0,
        dt=1.0 / 60.0,
    )

    assert 0.0 < low_probability < high_probability < 1.0


def test_capture_hazard_contains_social_multipliers() -> None:
    result = calculate_capture_hazard(
        baseline_hazard=4.0,
        exposure=1.0,
        dilution=0.0,
        confusion=0.0,
        crowding=0.0,
        exposure_strength=1.5,
        dilution_strength=0.35,
        confusion_strength=0.35,
        crowding_strength=0.75,
    )

    assert result["exposure_multiplier"] == 2.5
    assert result["dilution_multiplier"] == 1.0
    assert result["confusion_multiplier"] == 1.0
    assert result["crowding_multiplier"] == 1.0
    assert result["dispersion_multiplier"] == 1.0
    assert result["cohesion_multiplier"] == 1.0
    assert result["capture_hazard"] == 10.0


def test_dispersion_and_poor_cohesion_increase_hazard() -> None:
    baseline = calculate_capture_hazard(
        baseline_hazard=4.0,
        exposure=0.0,
        dilution=0.0,
        confusion=0.0,
        crowding=0.0,
        exposure_strength=1.5,
        dilution_strength=0.35,
        confusion_strength=0.35,
        crowding_strength=0.75,
        dispersion=0.0,
        cohesion=0.0,
        dispersion_strength=0.5,
        cohesion_strength=0.5,
    )
    poor_social_state = calculate_capture_hazard(
        baseline_hazard=4.0,
        exposure=0.0,
        dilution=0.0,
        confusion=0.0,
        crowding=0.0,
        exposure_strength=1.5,
        dilution_strength=0.35,
        confusion_strength=0.35,
        crowding_strength=0.75,
        dispersion=1.0,
        cohesion=1.0,
        dispersion_strength=0.5,
        cohesion_strength=0.5,
    )

    assert baseline["capture_hazard"] == 4.0
    assert poor_social_state["dispersion_multiplier"] == 1.5
    assert poor_social_state["cohesion_multiplier"] == 1.5
    assert poor_social_state["capture_hazard"] == 9.0


def test_crowding_increases_hazard_when_other_factors_are_equal() -> None:
    shared_parameters = {
        "baseline_hazard": 4.0,
        "exposure": 0.5,
        "dilution": 0.2,
        "confusion": 0.3,
        "exposure_strength": 1.5,
        "dilution_strength": 0.35,
        "confusion_strength": 0.35,
        "crowding_strength": 0.75,
        "dispersion": 0.2,
        "cohesion": 0.2,
        "dispersion_strength": 0.5,
        "cohesion_strength": 0.5,
    }

    lower_crowding = calculate_capture_hazard(
        **shared_parameters,
        crowding=0.1,
    )
    higher_crowding = calculate_capture_hazard(
        **shared_parameters,
        crowding=0.9,
    )

    assert (
        higher_crowding["crowding_multiplier"]
        > lower_crowding["crowding_multiplier"]
    )
    assert (
        higher_crowding["capture_hazard"]
        > lower_crowding["capture_hazard"]
    )


def test_isolated_fish_has_higher_risk_than_socially_protected_fish() -> None:
    config = SimulationConfig(
        fish_count=2,
        predator_count=1,
        random_perturbation=False,
    )

    predator = make_predator((550.0, 350.0))
    isolated_target = make_fish(0, (500.0, 350.0), (100.0, 0.0))
    grouped_neighbor = make_fish(1, (530.0, 350.0), (100.0, 0.0))

    isolated_risk = calculate_capture_risk(
        target=isolated_target,
        predator=predator,
        all_fish=[isolated_target],
        config=config,
        dt=1.0 / 60.0,
    )
    grouped_risk = calculate_capture_risk(
        target=isolated_target,
        predator=predator,
        all_fish=[isolated_target, grouped_neighbor],
        config=config,
        dt=1.0 / 60.0,
    )

    assert isolated_risk["dispersion"] == 1.0
    assert isolated_risk["cohesion"] == 1.0
    assert grouped_risk["dispersion"] < isolated_risk["dispersion"]
    assert grouped_risk["cohesion"] < isolated_risk["cohesion"]
    assert isolated_risk["capture_hazard"] > grouped_risk["capture_hazard"]
    assert (
        isolated_risk["capture_probability"]
        > grouped_risk["capture_probability"]
    )


def test_extreme_crowding_increases_crowding_risk_score() -> None:
    config = SimulationConfig(
        fish_count=4,
        predator_count=1,
        random_perturbation=False,
    )
    predator = make_predator((550.0, 350.0))
    target = make_fish(0, (500.0, 350.0), (100.0, 0.0))

    moderate_neighbors = [
        make_fish(1, (500.0, 370.0), (100.0, 0.0)),
        make_fish(2, (500.0, 330.0), (100.0, 0.0)),
        make_fish(3, (480.0, 350.0), (100.0, 0.0)),
    ]
    crowded_neighbors = [
        make_fish(1, (508.0, 350.0), (100.0, 0.0)),
        make_fish(2, (492.0, 350.0), (100.0, 0.0)),
        make_fish(3, (500.0, 358.0), (100.0, 0.0)),
    ]

    moderate_risk = calculate_capture_risk(
        target=target,
        predator=predator,
        all_fish=[target, *moderate_neighbors],
        config=config,
        dt=1.0 / 60.0,
    )
    crowded_risk = calculate_capture_risk(
        target=target,
        predator=predator,
        all_fish=[target, *crowded_neighbors],
        config=config,
        dt=1.0 / 60.0,
    )

    assert crowded_risk["crowding"] > moderate_risk["crowding"]
    assert (
        crowded_risk["crowding_multiplier"]
        > moderate_risk["crowding_multiplier"]
    )


def test_capture_attempt_is_logged_when_capture_fails() -> None:
    config = SimulationConfig(
        fish_count=1,
        predator_count=1,
        predation_baseline_hazard=0.0,
        random_perturbation=False,
    )

    world = World(config, seed=42)
    fish = world.fish[0]
    predator = world.predators[0]

    fish.position = pygame.Vector2(500.0, 350.0)
    predator.position = pygame.Vector2(510.0, 350.0)

    world._handle_captures()

    assert len(world.capture_attempts) == 1

    attempt = world.capture_attempts[0]
    assert attempt["fish_id"] == fish.fish_id
    assert attempt["predator_id"] == predator.id
    assert attempt["captured"] is False
    assert attempt["capture_hazard"] == 0.0
    assert attempt["capture_probability"] == 0.0
    assert len(world.capture_events) == 0


def test_successful_capture_is_logged_and_removed() -> None:
    config = SimulationConfig(
        fish_count=1,
        predator_count=1,
        predation_baseline_hazard=1_000_000_000.0,
        random_perturbation=False,
    )

    world = World(config, seed=42)
    fish = world.fish[0]
    predator = world.predators[0]

    fish.position = pygame.Vector2(500.0, 350.0)
    predator.position = pygame.Vector2(510.0, 350.0)

    world._handle_captures()

    assert len(world.capture_attempts) == 1
    assert world.capture_attempts[0]["captured"] is True
    assert len(world.capture_events) == 1
    assert len(world.fish) == 0