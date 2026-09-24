import math
import random
from typing import TYPE_CHECKING, Optional

import pygame

from schoolmind.simulation.physics import (
    adjust_direction_for_boundary,
    constrain_to_bounds,
    update_velocity,
)

if TYPE_CHECKING:
    from schoolmind.simulation.fish import Fish


class Predator:
    def __init__(
        self,
        predator_id: int,
        position: pygame.Vector2,
        max_speed: float,
        max_acceleration: float,
        detection_range: float,
        capture_radius: float,
        capture_cooldown: float,
        world_width: int,
        world_height: int,
        boundary_margin: float,
        rng: random.Random | None = None,
    ) -> None:
        self.id = predator_id

        self.position = position
        self.max_speed = max_speed
        self.max_acceleration = max_acceleration
        self.detection_range = detection_range
        self.capture_radius = capture_radius
        self.capture_cooldown = capture_cooldown
        self.capture_cooldown_remaining = 0.0

        self.world_width = world_width
        self.world_height = world_height
        self.boundary_margin = boundary_margin

        self.target: Optional["Fish"] = None
        self.target_switches = 0

        self.rng = (
            rng
            if rng is not None
            else random.Random()
        )

        # Start moving in a random direction.
        angle = self.rng.uniform(
            0,
            2 * math.pi,
        )

        direction = pygame.Vector2(
            math.cos(angle),
            math.sin(angle),
        )

        self.velocity = (
            direction * self.max_speed
        )

    def choose_target(
        self,
        fish: list["Fish"],
        unavailable_targets: Optional[set["Fish"]] = None,
    ) -> None:
        """Choose the nearest unclaimed fish within detection range."""
        if unavailable_targets is None:
            unavailable_targets = set()

        visible_fish = [
            candidate
            for candidate in fish
            if self.position.distance_to(
                candidate.position
            )
            <= self.detection_range
        ]

        unclaimed_visible = [
            candidate
            for candidate in visible_fish
            if candidate not in unavailable_targets
        ]

        # Prefer unique targets, but allow sharing when every
        # visible fish is already claimed.
        candidates = (
            unclaimed_visible
            or visible_fish
        )

        nearest_fish = None
        nearest_distance = self.detection_range

        for candidate in candidates:
            distance = self.position.distance_to(
                candidate.position
            )

            if distance <= nearest_distance:
                nearest_distance = distance
                nearest_fish = candidate

        if (
            self.target is not None
            and nearest_fish is not self.target
        ):
            self.target_switches += 1

        self.target = nearest_fish

    def get_desired_direction(
        self,
    ) -> Optional[pygame.Vector2]:
        """Return the direction toward the current target."""
        if self.target is None:
            return None

        direction = (
            self.target.position
            - self.position
        )

        if direction.length_squared() == 0:
            return None

        return direction.normalize()

    def update_capture_cooldown(
        self,
        dt: float,
    ) -> None:
        """Decrease the remaining capture cooldown."""
        self.capture_cooldown_remaining = max(
            0.0,
            self.capture_cooldown_remaining - dt,
        )

    def can_capture(self) -> bool:
        """Return whether this predator can currently capture a fish."""
        return (
            self.capture_cooldown_remaining <= 0.0
        )

    def register_capture(self) -> None:
        """Start the capture cooldown after a successful capture."""
        self.capture_cooldown_remaining = (
            self.capture_cooldown
        )

    def update(
        self,
        dt: float,
        desired_direction: Optional[pygame.Vector2],
    ) -> None:
        """Update predator movement for one simulation step."""
        if desired_direction is None:
            if self.velocity.length_squared() == 0:
                desired_direction = pygame.Vector2(1, 0)
            else:
                desired_direction = (
                    self.velocity.normalize()
                )

        desired_direction = adjust_direction_for_boundary(
            desired_direction=desired_direction,
            current_velocity=self.velocity,
            position=self.position,
            world_width=self.world_width,
            world_height=self.world_height,
            boundary_margin=self.boundary_margin,
        )

        self.velocity = update_velocity(
            velocity=self.velocity,
            desired_direction=desired_direction,
            target_speed=self.max_speed,
            max_speed=self.max_speed,
            max_acceleration=self.max_acceleration,
            dt=dt,
        )

        self.position += self.velocity * dt

        self.velocity = constrain_to_bounds(
            position=self.position,
            velocity=self.velocity,
            world_width=self.world_width,
            world_height=self.world_height,
            radius=0.0,
        )