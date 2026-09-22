import math
import random
from typing import Optional, TYPE_CHECKING

import pygame

from schoolmind.simulation.physics import update_velocity

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
        world_width: int,
        world_height: int,
    ) -> None:
        self.id = predator_id

        self.position = position

        self.max_speed = max_speed
        self.max_acceleration = max_acceleration

        self.detection_range = detection_range
        self.capture_radius = capture_radius

        self.world_width = world_width
        self.world_height = world_height

        self.target: Optional["Fish"] = None
        self.target_switches = 0

        # Start moving in a random direction.
        angle = random.uniform(0, 2 * math.pi)

        direction = pygame.Vector2(
            math.cos(angle),
            math.sin(angle),
        )

        self.velocity = direction * self.max_speed

    def choose_target(self, fish: list["Fish"]) -> None:
        """Choose the nearest fish within detection range."""

        nearest_fish = None
        nearest_distance = self.detection_range

        for candidate in fish:
            distance = self.position.distance_to(candidate.position)

            if distance <= nearest_distance:
                nearest_distance = distance
                nearest_fish = candidate

        if (
            self.target is not None
            and nearest_fish is not self.target
        ):
            self.target_switches += 1

        self.target = nearest_fish

    def get_desired_direction(self) -> Optional[pygame.Vector2]:
        """Return the direction toward the current target."""

        if self.target is None:
            return None

        direction = self.target.position - self.position

        if direction.length_squared() == 0:
            return None

        return direction.normalize()

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
                desired_direction = self.velocity.normalize()

        self.velocity = update_velocity(
            velocity=self.velocity,
            desired_direction=desired_direction,
            target_speed=self.max_speed,
            max_speed=self.max_speed,
            max_acceleration=self.max_acceleration,
            dt=dt,
        )

        self.position += self.velocity * dt

        self._wrap_position()

    def _wrap_position(self) -> None:
        self.position.x %= self.world_width
        self.position.y %= self.world_height