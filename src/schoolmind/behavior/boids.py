from __future__ import annotations
from typing import TYPE_CHECKING
from typing import Optional
import pygame

if TYPE_CHECKING:
    from schoolmind.simulation.fish import Fish


def _safe_normalize(vector: pygame.Vector2) -> pygame.Vector2:
    """Return a unit vector, or zero if the vector has no direction."""
    if vector.length_squared() == 0:
        return pygame.Vector2()

    return vector.normalize()


def get_neighbors(
    fish: Fish,
    all_fish: list[Fish],
    neighbor_radius: float,
) -> list[Fish]:
    """Return all fish within the local neighborhood."""
    neighbors: list[Fish] = []

    for other in all_fish:
        if other is fish:
            continue

        distance = fish.position.distance_to(other.position)

        if distance <= neighbor_radius:
            neighbors.append(other)

    return neighbors


def calculate_separation(
    fish: Fish,
    neighbors: list[Fish],
    separation_radius: float,
) -> pygame.Vector2:
    """Return a direction that pushes the fish away from nearby neighbors."""
    force = pygame.Vector2()

    for neighbor in neighbors:
        offset = fish.position - neighbor.position
        distance = offset.length()

        if distance == 0:
            continue

        if distance < separation_radius:
            force += offset.normalize() / distance

    return _safe_normalize(force)


def calculate_alignment(
    neighbors: list[Fish],
) -> pygame.Vector2:
    """Return the average direction of neighboring fish."""
    if not neighbors:
        return pygame.Vector2()

    average_velocity = pygame.Vector2()

    for neighbor in neighbors:
        average_velocity += neighbor.velocity

    average_velocity /= len(neighbors)

    return _safe_normalize(average_velocity)


def calculate_cohesion(
    fish: Fish,
    neighbors: list[Fish],
) -> pygame.Vector2:
    """Return a direction toward the center of the local group."""
    if not neighbors:
        return pygame.Vector2()

    center = pygame.Vector2()

    for neighbor in neighbors:
        center += neighbor.position

    center /= len(neighbors)

    direction_to_center = center - fish.position

    return _safe_normalize(direction_to_center)


def calculate_desired_direction(
    fish: Fish,
    all_fish: list[Fish],
    neighbor_radius: float,
    separation_radius: float,
    separation_weight: float,
    alignment_weight: float,
    cohesion_weight: float,
) -> Optional[pygame.Vector2]:
    """Combine the three boids rules into one desired direction."""

    neighbors = get_neighbors(
        fish,
        all_fish,
        neighbor_radius,
    )

    if not neighbors:
        return None

    separation = calculate_separation(
        fish,
        neighbors,
        separation_radius,
    )

    alignment = calculate_alignment(neighbors)

    cohesion = calculate_cohesion(
        fish,
        neighbors,
    )

    combined = (
        separation * separation_weight
        + alignment * alignment_weight
        + cohesion * cohesion_weight
    )

    if combined.length_squared() == 0:
        return None

    return combined.normalize()