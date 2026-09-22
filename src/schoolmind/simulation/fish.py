import math
import random
from typing import Optional
import pygame
from schoolmind.simulation.physics import update_velocity

class Fish:
    def __init__(
        self,
        position: pygame.Vector2,
        target_speed: float,
        max_speed: float,
        max_acceleration: float,
        max_turn_rate: float,
        world_width: int,
        world_height: int,
        random_perturbation: bool = True,
    ) -> None:
        self.position = position

        self.target_speed = target_speed
        self.max_speed = max_speed
        self.max_acceleration = max_acceleration
        self.max_turn_rate = max_turn_rate
        self.random_perturbation = random_perturbation

        self.world_width = world_width
        self.world_height = world_height

        # Start in a random direction.
        angle = random.uniform(0, 2 * math.pi)

        direction = pygame.Vector2(
            math.cos(angle),
            math.sin(angle),
        )

        # Start already moving at the target speed.
        self.velocity = direction * self.target_speed

    def update(
        self,
        dt: float,
        desired_direction: Optional[pygame.Vector2] = None,
    ) -> None:
        """Update the fish for one simulation step."""

        if self.velocity.length_squared() == 0:
            current_direction = pygame.Vector2(1, 0)
        else:
            current_direction = self.velocity.normalize()

        if desired_direction is None:
            if self.random_perturbation:
                turn_amount = random.uniform(
                    -self.max_turn_rate,
                    self.max_turn_rate,
                ) * dt
            else:
                turn_amount = 0.0

            desired_direction = current_direction.rotate_rad(turn_amount)

        self.velocity = update_velocity(
            velocity=self.velocity,
            desired_direction=desired_direction,
            target_speed=self.target_speed,
            max_speed=self.max_speed,
            max_acceleration=self.max_acceleration,
            dt=dt,
        )

        self.position += self.velocity * dt

        self._wrap_position()

    def _wrap_position(self) -> None:
        self.position.x %= self.world_width
        self.position.y %= self.world_height