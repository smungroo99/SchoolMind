from __future__ import annotations

import pygame
from typing import Optional, TYPE_CHECKING
from schoolmind.simulation.predator import Predator


def _safe_normalize(vector: pygame.Vector2) -> pygame.Vector2:
    """Return a unit vector, or zero if the vector has no direction."""
    if vector.length_squared() == 0:
        return pygame.Vector2()

    return vector.normalize()


def calculate_separation(
    predator: Predator,
    predators: list[Predator],
    separation_radius: float,
) -> pygame.Vector2:
    """Return a direction that pushes a predator away from nearby predators."""

    force = pygame.Vector2()

    for other in predators:
        if other is predator:
            continue

        offset = predator.position - other.position
        distance = offset.length()

        if distance == 0:
            continue

        if distance < separation_radius:
            force += offset.normalize() / distance

    return _safe_normalize(force)