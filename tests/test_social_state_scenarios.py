
import pygame

from schoolmind.simulation.config import SimulationConfig
from schoolmind.simulation.fish import Fish
from schoolmind.simulation.predator import Predator
from schoolmind.simulation.predation_risk import calculate_capture_risk


def make_fish(
    fish_id: int,
    position: tuple[float, float],
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
    fish.velocity = pygame.Vector2(100.0, 0.0)
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


def calculate_scenario_risk(
    neighbor_offsets: list[tuple[float, float]],
) -> dict:
    """
    Calculate risk for a target at a fixed position.

    Neighbor offsets define the social configuration. The
    predator always stays east of the target, and all fish
    have the same velocity. This keeps the setup comparable
    across scenarios.
    """
    config = SimulationConfig(
        fish_count=len(neighbor_offsets) + 1,
        predator_count=1,
        random_perturbation=False,
    )

    target_x = 500.0
    target_y = 350.0
    social_radius = config.predation_social_radius

    target = make_fish(
        0,
        (target_x, target_y),
    )

    neighbors = [
        make_fish(
            fish_id=index + 1,
            position=(
                target_x + offset_x,
                target_y + offset_y,
            ),
        )
        for index, (offset_x, offset_y)
        in enumerate(neighbor_offsets)
    ]

    predator = make_predator(
        (
            target_x + 2.0 * social_radius,
            target_y,
        )
    )

    return calculate_capture_risk(
        target=target,
        predator=predator,
        all_fish=[target, *neighbors],
        config=config,
        dt=1.0 / 60.0,
    )


def test_combined_social_scenarios_have_expected_risk_order() -> None:
    """
    A well-spaced group should outperform an isolated,
    dispersed, or excessively crowded social configuration.

    This compares the current model's combined effects;
    it does not claim these parameters are biologically optimal.
    """
    isolated = calculate_scenario_risk(
        neighbor_offsets=[],
    )

    radius = SimulationConfig().predation_social_radius

    dispersed = calculate_scenario_risk(
        neighbor_offsets=[
            (-0.8 * radius, 0.0),
            (-0.6 * radius, 0.0),
        ],
    )

    well_grouped = calculate_scenario_risk(
        neighbor_offsets=[
            (0.0, -0.2 * radius),
            (0.0, 0.2 * radius),
            (-0.2 * radius, 0.0),
            (0.2 * radius, 0.0),
        ],
    )

    crowd_offset = max(
        6.0,
        0.06 * radius,
    )

    overcrowded = calculate_scenario_risk(
        neighbor_offsets=[
            (-crowd_offset, 0.0),
            (crowd_offset, 0.0),
            (0.0, -crowd_offset),
            (0.0, crowd_offset),
        ],
    )

    assert isolated["neighbor_count"] == 0
    assert isolated["dispersion"] == 1.0
    assert isolated["cohesion"] == 1.0

    assert dispersed["neighbor_count"] == 2
    assert dispersed["dispersion"] > well_grouped["dispersion"]
    assert dispersed["cohesion"] > well_grouped["cohesion"]

    assert well_grouped["neighbor_count"] == 4
    assert well_grouped["cohesion_distance"] < 1e-6

    assert overcrowded["neighbor_count"] == 4
    assert (
        overcrowded["nearest_neighbor_distance"]
        < well_grouped["nearest_neighbor_distance"]
    )
    assert overcrowded["crowding"] > well_grouped["crowding"]

    # Validate the net effect after all social-risk
    # mechanisms have been combined.
    assert (
        isolated["capture_hazard"]
        > dispersed["capture_hazard"]
    )
    assert (
        dispersed["capture_hazard"]
        > well_grouped["capture_hazard"]
    )
    assert (
        overcrowded["capture_hazard"]
        > well_grouped["capture_hazard"]
    )

    assert (
        isolated["capture_probability"]
        > dispersed["capture_probability"]
        > well_grouped["capture_probability"]
    )
    assert (
        overcrowded["capture_probability"]
        > well_grouped["capture_probability"]
    )
