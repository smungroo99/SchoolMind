
import math

import pygame

from schoolmind.simulation.fish import Fish
from schoolmind.simulation.predator import Predator
from schoolmind.simulation.predation_risk import (
    calculate_capture_hazard,
    calculate_capture_probability,
    calculate_cohesion,
    calculate_confusion,
    calculate_crowding,
    calculate_dilution,
    calculate_dispersion,
    calculate_exposure,
)


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


def calculate_hazard(
    **overrides: float,
) -> dict[str, float]:
    """Calculate hazard with all unspecified social effects fixed."""
    inputs: dict[str, float] = {
        "baseline_hazard": 4.0,
        "exposure": 0.0,
        "dilution": 0.0,
        "confusion": 0.0,
        "crowding": 0.0,
        "dispersion": 0.0,
        "cohesion": 0.0,
        "exposure_strength": 1.5,
        "dilution_strength": 0.35,
        "confusion_strength": 0.35,
        "crowding_strength": 0.75,
        "dispersion_strength": 0.5,
        "cohesion_strength": 0.5,
    }
    inputs.update(overrides)
    return calculate_capture_hazard(**inputs)


def report_comparison(
    name: str,
    favorable_label: str,
    unfavorable_label: str,
    favorable_score: float,
    unfavorable_score: float,
    favorable_hazard: dict[str, float],
    unfavorable_hazard: dict[str, float],
) -> None:
    favorable_probability = calculate_capture_probability(
        favorable_hazard["capture_hazard"],
        1.0 / 60.0,
    )
    unfavorable_probability = calculate_capture_probability(
        unfavorable_hazard["capture_hazard"],
        1.0 / 60.0,
    )

    print(f"{name}")
    print(
        f"  {favorable_label}: score={favorable_score:.4f}, "
        f"hazard={favorable_hazard['capture_hazard']:.4f}, "
        f"probability={favorable_probability:.6f}"
    )
    print(
        f"  {unfavorable_label}: score={unfavorable_score:.4f}, "
        f"hazard={unfavorable_hazard['capture_hazard']:.4f}, "
        f"probability={unfavorable_probability:.6f}"
    )

    passed = (
        unfavorable_hazard["capture_hazard"]
        > favorable_hazard["capture_hazard"]
        and unfavorable_probability > favorable_probability
    )
    print(f"  Result: {'PASS' if passed else 'FAIL'}")
    print()

    if not passed:
        raise AssertionError(
            f"{name}: the unfavorable state did not increase "
            "capture hazard and capture probability."
        )


def test_dispersion() -> None:
    social_radius = 100.0

    close_score = calculate_dispersion(
        neighbor_count=2,
        mean_neighbor_distance=20.0,
        social_radius=social_radius,
    )
    dispersed_score = calculate_dispersion(
        neighbor_count=2,
        mean_neighbor_distance=80.0,
        social_radius=social_radius,
    )

    close_hazard = calculate_hazard(
        dispersion=close_score,
    )
    dispersed_hazard = calculate_hazard(
        dispersion=dispersed_score,
    )

    assert dispersed_score > close_score

    report_comparison(
        "1. Dispersion",
        "Less dispersed",
        "More dispersed",
        close_score,
        dispersed_score,
        close_hazard,
        dispersed_hazard,
    )


def test_cohesion() -> None:
    social_radius = 100.0

    centered_score = calculate_cohesion(
        neighbor_count=2,
        cohesion_distance=10.0,
        social_radius=social_radius,
    )
    distant_score = calculate_cohesion(
        neighbor_count=2,
        cohesion_distance=80.0,
        social_radius=social_radius,
    )

    centered_hazard = calculate_hazard(
        cohesion=centered_score,
    )
    distant_hazard = calculate_hazard(
        cohesion=distant_score,
    )

    assert distant_score > centered_score

    report_comparison(
        "2. Cohesion",
        "Closer to group center",
        "Farther from group center",
        centered_score,
        distant_score,
        centered_hazard,
        distant_hazard,
    )


def test_alignment() -> None:
    target = make_fish(
        0,
        (500.0, 350.0),
        (100.0, 0.0),
    )
    predator = make_predator(
        (550.0, 350.0)
    )

    # Positions are identical; only neighbor velocity changes.
    aligned_neighbor = make_fish(
        1,
        (500.0, 360.0),
        (100.0, 0.0),
    )
    misaligned_neighbor = make_fish(
        1,
        (500.0, 360.0),
        (0.0, 100.0),
    )

    aligned_confusion = calculate_confusion(
        target=target,
        predator=predator,
        neighbors=[aligned_neighbor],
        distance_scale=50.0,
        saturation=4.0,
    )
    misaligned_confusion = calculate_confusion(
        target=target,
        predator=predator,
        neighbors=[misaligned_neighbor],
        distance_scale=50.0,
        saturation=4.0,
    )

    # Alignment is currently represented through confusion,
    # not through a separate alignment-risk multiplier.
    assert aligned_confusion > misaligned_confusion

    aligned_hazard = calculate_hazard(
        confusion=aligned_confusion,
    )
    misaligned_hazard = calculate_hazard(
        confusion=misaligned_confusion,
    )

    report_comparison(
        "3. Alignment (via predator confusion)",
        "Aligned movement",
        "Misaligned movement",
        aligned_confusion,
        misaligned_confusion,
        aligned_hazard,
        misaligned_hazard,
    )


def test_crowding() -> None:
    less_crowded_score = calculate_crowding(
        nearest_neighbor_distance=100.0,
        crowding_distance=15.0,
        crowding_scale=5.0,
    )
    crowded_score = calculate_crowding(
        nearest_neighbor_distance=5.0,
        crowding_distance=15.0,
        crowding_scale=5.0,
    )

    less_crowded_hazard = calculate_hazard(
        crowding=less_crowded_score,
    )
    crowded_hazard = calculate_hazard(
        crowding=crowded_score,
    )

    assert crowded_score > less_crowded_score

    report_comparison(
        "4. Crowding",
        "More space",
        "Very close neighbors",
        less_crowded_score,
        crowded_score,
        less_crowded_hazard,
        crowded_hazard,
    )


def test_dilution() -> None:
    no_neighbors_score = calculate_dilution(
        neighbor_count=0,
        saturation=4.0,
    )
    grouped_score = calculate_dilution(
        neighbor_count=4,
        saturation=4.0,
    )

    no_neighbors_hazard = calculate_hazard(
        dilution=no_neighbors_score,
    )
    grouped_hazard = calculate_hazard(
        dilution=grouped_score,
    )

    assert grouped_score > no_neighbors_score

    report_comparison(
        "5. Dilution",
        "Nearby alternatives present",
        "No nearby alternatives",
        grouped_score,
        no_neighbors_score,
        grouped_hazard,
        no_neighbors_hazard,
    )


def test_shielding() -> None:
    target = make_fish(
        0,
        (500.0, 350.0),
        (100.0, 0.0),
    )
    predator = make_predator(
        (550.0, 350.0)
    )

    # A valid shield is between the target and predator.
    shielding_neighbor = make_fish(
        1,
        (525.0, 350.0),
        (100.0, 0.0),
    )

    # This neighbor lies beyond the predator.
    behind_predator_neighbor = make_fish(
        2,
        (575.0, 350.0),
        (100.0, 0.0),
    )

    shielded_exposure = calculate_exposure(
        target=target,
        predator=predator,
        neighbors=[shielding_neighbor],
        exposure_radius=100.0,
        exposure_saturation=2.0,
    )
    unshielded_exposure = calculate_exposure(
        target=target,
        predator=predator,
        neighbors=[behind_predator_neighbor],
        exposure_radius=100.0,
        exposure_saturation=2.0,
    )

    assert shielded_exposure < unshielded_exposure

    shielded_hazard = calculate_hazard(
        exposure=shielded_exposure,
    )
    unshielded_hazard = calculate_hazard(
        exposure=unshielded_exposure,
    )

    report_comparison(
        "6. Geometric shielding",
        "Neighbor blocks the predator-target line",
        "Neighbor is behind the predator",
        shielded_exposure,
        unshielded_exposure,
        shielded_hazard,
        unshielded_hazard,
    )


def main() -> None:
    pygame.init()

    print("SchoolMind: independent social-risk factor validation")
    print("Each comparison changes one hazard input at a time.")
    print("These checks validate formula behavior, not biological accuracy.")
    print()

    tests = [
        test_dispersion,
        test_cohesion,
        test_alignment,
        test_crowding,
        test_dilution,
        test_shielding,
    ]

    for test in tests:
        test()

    print(f"All {len(tests)} independent factor checks passed.")


if __name__ == "__main__":
    main()