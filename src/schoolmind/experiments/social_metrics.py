from statistics import mean
from typing import Any

import pygame

from schoolmind.behavior.boids import get_neighbors
from schoolmind.simulation.fish import Fish
from schoolmind.simulation.world import World


def _mean_or_none(
    values: list[float],
) -> float | None:
    if not values:
        return None

    return mean(values)


def calculate_fish_social_state(
    fish: Fish,
    all_fish: list[Fish],
    neighbor_radius: float,
) -> dict[str, Any]:
    """
    Calculate the local social state of one fish.

    These measurements are observational only.
    They do not affect the fish's behavior.
    """
    neighbors = get_neighbors(
        fish=fish,
        all_fish=all_fish,
        neighbor_radius=neighbor_radius,
    )

    neighbor_count = len(neighbors)

    if not neighbors:
        return {
            "neighbor_count": 0,
            "nearest_neighbor_distance": None,
            "mean_neighbor_distance": None,
            "alignment": None,
            "cohesion_distance": None,
        }

    distances = [
        fish.position.distance_to(
            neighbor.position
        )
        for neighbor in neighbors
    ]

    nearest_neighbor_distance = min(
        distances
    )

    mean_neighbor_distance = mean(
        distances
    )

    alignment_scores: list[float] = []

    if fish.velocity.length_squared() > 0:
        fish_direction = (
            fish.velocity.normalize()
        )

        for neighbor in neighbors:
            if (
                neighbor.velocity.length_squared()
                == 0
            ):
                continue

            neighbor_direction = (
                neighbor.velocity.normalize()
            )

            cosine_similarity = (
                fish_direction.dot(
                    neighbor_direction
                )
            )

            alignment_score = (
                cosine_similarity + 1.0
            ) / 2.0

            alignment_scores.append(
                alignment_score
            )

    alignment = _mean_or_none(
        alignment_scores
    )

    local_center = pygame.Vector2()

    for neighbor in neighbors:
        local_center += neighbor.position

    local_center /= len(neighbors)

    cohesion_distance = (
        fish.position.distance_to(
            local_center
        )
    )

    return {
        "neighbor_count": neighbor_count,
        "nearest_neighbor_distance": (
            nearest_neighbor_distance
        ),
        "mean_neighbor_distance": (
            mean_neighbor_distance
        ),
        "alignment": alignment,
        "cohesion_distance": (
            cohesion_distance
        ),
    }


def calculate_school_social_metrics(
    world: World,
) -> dict[str, Any]:
    """
    Calculate aggregate social metrics for
    all living fish in the current world.
    """
    fish = world.fish

    if not fish:
        return {
            "fish_count": 0,
            "isolated_fish_fraction": 0.0,
            "mean_neighbor_count": None,
            "mean_nearest_neighbor_distance": None,
            "mean_neighbor_distance": None,
            "mean_alignment": None,
            "mean_cohesion_distance": None,
            "polarization": None,
            "dispersion": None,
        }

    states = [
        calculate_fish_social_state(
            fish=current_fish,
            all_fish=fish,
            neighbor_radius=(
                world.config.neighbor_radius
            ),
        )
        for current_fish in fish
    ]

    neighbor_counts = [
        state["neighbor_count"]
        for state in states
    ]

    nearest_neighbor_distances = [
        state["nearest_neighbor_distance"]
        for state in states
        if state[
            "nearest_neighbor_distance"
        ] is not None
    ]

    mean_neighbor_distances = [
        state["mean_neighbor_distance"]
        for state in states
        if state[
            "mean_neighbor_distance"
        ] is not None
    ]

    alignments = [
        state["alignment"]
        for state in states
        if state["alignment"] is not None
    ]

    cohesion_distances = [
        state["cohesion_distance"]
        for state in states
        if state[
            "cohesion_distance"
        ] is not None
    ]

    isolated_fish_count = sum(
        1
        for state in states
        if state["neighbor_count"] == 0
    )

    isolated_fish_fraction = (
        isolated_fish_count
        / len(states)
    )

    # --------------------------------------------------------------
    # Polarization
    # --------------------------------------------------------------

    direction_sum = pygame.Vector2()
    moving_fish_count = 0

    for current_fish in fish:
        if (
            current_fish.velocity.length_squared()
            == 0
        ):
            continue

        direction_sum += (
            current_fish.velocity.normalize()
        )

        moving_fish_count += 1

    if moving_fish_count == 0:
        polarization = None
    else:
        polarization = (
            direction_sum.length()
            / moving_fish_count
        )

    # --------------------------------------------------------------
    # Dispersion
    # --------------------------------------------------------------

    school_centroid = pygame.Vector2()

    for current_fish in fish:
        school_centroid += current_fish.position

    school_centroid /= len(fish)

    distances_from_centroid = [
        current_fish.position.distance_to(
            school_centroid
        )
        for current_fish in fish
    ]

    dispersion = mean(
        distances_from_centroid
    )

    return {
        "fish_count": len(fish),
        "isolated_fish_fraction": (
            isolated_fish_fraction
        ),
        "mean_neighbor_count": mean(
            neighbor_counts
        ),
        "mean_nearest_neighbor_distance": (
            _mean_or_none(
                nearest_neighbor_distances
            )
        ),
        "mean_neighbor_distance": (
            _mean_or_none(
                mean_neighbor_distances
            )
        ),
        "mean_alignment": (
            _mean_or_none(alignments)
        ),
        "mean_cohesion_distance": (
            _mean_or_none(
                cohesion_distances
            )
        ),
        "polarization": polarization,
        "dispersion": dispersion,
    }


def collect_school_social_snapshot(
    world: World,
) -> dict[str, Any]:
    """
    Collect one timestamped school-level snapshot.
    """
    return {
        "time": world.elapsed_time,
        **calculate_school_social_metrics(world),
    }


def collect_individual_social_snapshot(
    world: World,
) -> list[dict[str, Any]]:
    """
    Collect one timestamped social-state record
    for every living fish.
    """
    snapshots: list[dict[str, Any]] = []

    for fish in world.fish:
        social_state = (
            calculate_fish_social_state(
                fish=fish,
                all_fish=world.fish,
                neighbor_radius=(
                    world.config.neighbor_radius
                ),
            )
        )

        snapshots.append(
            {
                "time": world.elapsed_time,
                "fish_id": fish.fish_id,
                **social_state,
            }
        )

    return snapshots