
import math
from statistics import mean
from typing import Any

import pygame

from schoolmind.simulation.config import SimulationConfig
from schoolmind.simulation.fish import Fish
from schoolmind.simulation.predator import Predator


def _clamp(
    value: float,
    minimum: float = 0.0,
    maximum: float = 1.0,
) -> float:
    return max(
        minimum,
        min(maximum, value),
    )


def _cosine_similarity(
    first: pygame.Vector2,
    second: pygame.Vector2,
) -> float:
    if (
        first.length_squared() == 0
        or second.length_squared() == 0
    ):
        return 0.0

    return _clamp(
        first.normalize().dot(
            second.normalize()
        ),
        -1.0,
        1.0,
    )


def _get_neighbors(
    target: Fish,
    all_fish: list[Fish],
    radius: float,
) -> list[Fish]:
    neighbors: list[Fish] = []
    for fish in all_fish:
        if fish is target:
            continue

        if (
            target.position.distance_to(
                fish.position
            )
            <= radius
        ):
            neighbors.append(fish)

    return neighbors


def _calculate_local_social_state(
    target: Fish,
    neighbors: list[Fish],
) -> dict[str, Any]:
    if not neighbors:
        return {
            "neighbor_count": 0,
            "nearest_neighbor_distance": None,
            "mean_neighbor_distance": None,
            "alignment": None,
            "cohesion_distance": None,
        }

    distances = [
        target.position.distance_to(
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

    if target.velocity.length_squared() > 0:
        for neighbor in neighbors:
            if neighbor.velocity.length_squared() == 0:
                continue

            cosine_similarity = (
                _cosine_similarity(
                    target.velocity,
                    neighbor.velocity,
                )
            )
            alignment_scores.append(
                (cosine_similarity + 1.0) / 2.0
            )

    alignment = (
        mean(alignment_scores)
        if alignment_scores
        else None
    )

    local_center = pygame.Vector2()

    for neighbor in neighbors:
        local_center += neighbor.position

    local_center /= len(neighbors)

    cohesion_distance = (
        target.position.distance_to(
            local_center
        )
    )
    return {
        "neighbor_count": len(neighbors),
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


def calculate_exposure(
    target: Fish,
    predator: Predator,
    neighbors: list[Fish],
    exposure_radius: float,
    exposure_saturation: float,
) -> float:
    """
    Estimate how exposed a target fish is to a predator.

    A neighbor contributes shielding only when:
    - Its center lies between the target and predator.
    - Its body intersects the direct line between them.
    - It is within the configured exposure radius of the target.

    A fish with no nearby shielding fish has exposure near 1.
    Nearby fish that genuinely obstruct the predator's view
    reduce exposure.

    Returns a value in [0, 1].
    """
    if exposure_radius <= 0:
        raise ValueError(
            "exposure_radius must be greater than zero."
        )

    if exposure_saturation <= 0:
        raise ValueError(
            "exposure_saturation must be greater than zero."
        )

    # Direction from the target toward the predator.
    target_to_predator = (
        predator.position - target.position
    )
    predator_distance = target_to_predator.length()

    if predator_distance == 0:
        return 1.0

    attack_direction = target_to_predator.normalize()
    shielding_signal = 0.0

    for neighbor in neighbors:
        offset = (
            neighbor.position - target.position
        )
        distance = offset.length()

        if distance == 0 or distance > exposure_radius:
            continue

        # Project the neighbor onto the line from the target
        # toward the predator. Its center must be between
        # the target and predator, not behind the predator.
        projection_distance = offset.dot(
            attack_direction
        )

        if (
            projection_distance <= 0
            or projection_distance >= predator_distance
        ):
            continue

        # Measure the perpendicular distance from the
        # neighbor's center to the predator-target line.
        perpendicular_offset = (
            offset
            - attack_direction * projection_distance
        )
        perpendicular_distance = (
            perpendicular_offset.length()
        )

        # The neighboring fish can shield the target only
        # if its body intersects the predator-target line.
        blocking_radius = float(neighbor.radius)

        if blocking_radius <= 0:
            if perpendicular_distance > 1e-9:
                continue
            line_weight = 1.0
        else:
            if perpendicular_distance >= blocking_radius:
                continue

            # Shielding decreases smoothly as the neighbor's
            # center approaches the edge of its blocking radius.
            line_weight = (
                1.0
                - perpendicular_distance / blocking_radius
            )

        # Alignment of the target-to-neighbor direction
        # with the target-to-predator direction.
        facing_alignment = (
            projection_distance / distance
        )

        proximity_weight = max(
            0.0,
            1.0 - distance / exposure_radius,
        )

        shielding_signal += (
            facing_alignment
            * proximity_weight
            * line_weight
        )

    shielding = 1.0 - math.exp(
        -shielding_signal / exposure_saturation
    )

    return _clamp(
        1.0 - shielding
    )


def calculate_dilution(
    neighbor_count: int,
    saturation: float,
) -> float:
    """
    Convert the number of nearby alternative prey into
    a bounded dilution-protection score.

    Returns 0 for an isolated fish and approaches 1 as
    nearby prey increase.
    """
    if saturation <= 0:
        raise ValueError(
            "Dilution saturation must be greater than zero."
        )

    if neighbor_count <= 0:
        return 0.0
    return _clamp(
        1.0 - math.exp(
            -neighbor_count / saturation
        )
    )


def calculate_confusion(
    target: Fish,
    predator: Predator,
    neighbors: list[Fish],
    distance_scale: float,
    saturation: float,
) -> float:
    """
    Estimate predator target ambiguity created by nearby fish.
    A neighboring fish contributes more when:
    - it is close to the target,
    - it is moving similarly to the target,
    - it appears in a similar visual direction from the predator.

    Returns a value in [0, 1].
    """
    if distance_scale <= 0:
        raise ValueError(
            "Confusion distance scale must be greater than zero."
        )

    if saturation <= 0:
        raise ValueError(
            "Confusion saturation must be greater than zero."
        )

    target_velocity = target.velocity

    target_from_predator = (
        target.position - predator.position
    )

    if target_from_predator.length_squared() > 0:
        target_view_direction = (
            target_from_predator.normalize()
        )
    else:
        target_view_direction = None

    competitor_signal = 0.0

    for neighbor in neighbors:
        target_distance = (
            target.position.distance_to(
                neighbor.position
            )
        )
        if target_distance == 0:
            continue

        movement_similarity = 0.0

        if (
            target_velocity.length_squared() > 0
            and neighbor.velocity.length_squared() > 0
        ):
            movement_similarity = max(
                0.0,
                _cosine_similarity(
                    target_velocity,
                    neighbor.velocity,
                ),
            )

        if movement_similarity == 0.0:
            continue

        neighbor_from_predator = (
            neighbor.position
            - predator.position
        )

        if (
            target_view_direction is None
            or neighbor_from_predator.length_squared() == 0
        ):
            view_similarity = 1.0
        else:
            view_similarity = max(
                0.0,
                target_view_direction.dot(
                    neighbor_from_predator.normalize()
                ),
            )

        distance_weight = math.exp(
            -target_distance
            / distance_scale
        )

        competitor_signal += (
            movement_similarity
            * view_similarity
            * distance_weight
        )

    return _clamp(
        1.0 - math.exp(
            -competitor_signal / saturation
        )
    )


def calculate_crowding(
    nearest_neighbor_distance: float | None,
    crowding_distance: float,
    crowding_scale: float,
) -> float:
    """
    Estimate excessive local crowding.

    A fish with no neighbors has zero crowding.
    Crowding rises smoothly as the nearest neighbor becomes
    very close.

    Returns a value in [0, 1].
    """
    if crowding_distance < 0:
        raise ValueError(
            "crowding_distance cannot be negative."
        )
    if crowding_scale <= 0:
        raise ValueError(
            "crowding_scale must be greater than zero."
        )

    if nearest_neighbor_distance is None:
        return 0.0

    exponent = (
        nearest_neighbor_distance
        - crowding_distance
    ) / crowding_scale

    return _clamp(
        1.0 / (
            1.0
            + math.exp(exponent)
        )
    )


def calculate_capture_hazard(
    baseline_hazard: float,
    exposure: float,
    dilution: float,
    confusion: float,
    crowding: float,
    exposure_strength: float,
    dilution_strength: float,
    confusion_strength: float,
    crowding_strength: float,
) -> dict[str, float]:
    """
    Combine the four independent social-risk mechanisms.

    The resulting hazard is:
        baseline
        * exposure multiplier
        * dilution multiplier
        * confusion multiplier
        * crowding multiplier

    Exposure and crowding increase hazard.
    Dilution and confusion decrease hazard.
    """
    if baseline_hazard < 0:
        raise ValueError(
            "baseline_hazard cannot be negative."
        )

    exposure_multiplier = (
        1.0
        + exposure_strength * exposure
    )
    dilution_multiplier = max(
        0.1,
        1.0
        - dilution_strength * dilution,
    )

    confusion_multiplier = max(
        0.1,
        1.0
        - confusion_strength * confusion,
    )

    crowding_multiplier = (
        1.0
        + crowding_strength * crowding
    )

    hazard = (
        baseline_hazard
        * exposure_multiplier
        * dilution_multiplier
        * confusion_multiplier
        * crowding_multiplier
    )
    return {
        "exposure_multiplier": (
            exposure_multiplier
        ),
        "dilution_multiplier": (
            dilution_multiplier
        ),
        "confusion_multiplier": (
            confusion_multiplier
        ),
        "crowding_multiplier": (
            crowding_multiplier
        ),
        "capture_hazard": hazard,
    }


def calculate_capture_probability(
    capture_hazard: float,
    dt: float,
) -> float:
    """
    Convert continuous-time capture hazard into the
    probability of capture during one simulation step.

        P(capture) = 1 - exp(-hazard * dt)
    """
    if capture_hazard < 0:
        raise ValueError(
            "capture_hazard cannot be negative."
        )

    if dt <= 0:
        raise ValueError(
            "dt must be greater than zero."
        )
    return _clamp(
        -math.expm1(
            -capture_hazard * dt
        )
    )


def calculate_capture_risk(
    target: Fish,
    predator: Predator,
    all_fish: list[Fish],
    config: SimulationConfig,
    dt: float,
) -> dict[str, Any]:
    """
    Calculate the complete predation-risk state for one
    predator-target capture check.

    This function is deterministic. Randomness is applied by
    World when the resulting capture probability is sampled.
    """
    neighbors = _get_neighbors(
        target=target,
        all_fish=all_fish,
        radius=config.predation_social_radius,
    )

    social_state = _calculate_local_social_state(
        target=target,
        neighbors=neighbors,
    )
    exposure = calculate_exposure(
        target=target,
        predator=predator,
        neighbors=neighbors,
        exposure_radius=(
            config.predation_social_radius
        ),
        exposure_saturation=(
            config.predation_exposure_saturation
        ),
    )

    dilution = calculate_dilution(
        neighbor_count=social_state[
            "neighbor_count"
        ],
        saturation=(
            config.predation_dilution_saturation
        ),
    )
    confusion = calculate_confusion(
        target=target,
        predator=predator,
        neighbors=neighbors,
        distance_scale=(
            config.predation_confusion_distance_scale
        ),
        saturation=(
            config.predation_confusion_saturation
        ),
    )
    crowding = calculate_crowding(
        nearest_neighbor_distance=(
            social_state[
                "nearest_neighbor_distance"
            ]
        ),
        crowding_distance=(
            config.predation_crowding_distance
        ),
        crowding_scale=(
            config.predation_crowding_scale
        ),
    )
    hazard_components = calculate_capture_hazard(
        baseline_hazard=(
            config.predation_baseline_hazard
        ),
        exposure=exposure,
        dilution=dilution,
        confusion=confusion,
        crowding=crowding,
        exposure_strength=(
            config.predation_exposure_strength
        ),
        dilution_strength=(
            config.predation_dilution_strength
        ),
        confusion_strength=(
            config.predation_confusion_strength
        ),
        crowding_strength=(
            config.predation_crowding_strength
        ),
    )
    capture_hazard = hazard_components[
        "capture_hazard"
    ]

    capture_probability = (
        calculate_capture_probability(
            capture_hazard=capture_hazard,
            dt=dt,
        )
    )
    return {
        "predator_distance": (
            predator.position.distance_to(
                target.position
            )
        ),
        **social_state,
        "exposure": exposure,
        "dilution": dilution,
        "confusion": confusion,
        "crowding": crowding,
        **hazard_components,
        "capture_probability": (
            capture_probability
        ),
    }