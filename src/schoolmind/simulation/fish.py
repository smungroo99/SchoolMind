import math
import random

import pygame


class Fish:
    def __init__(
        self,
        position: pygame.Vector2,
        speed: float,
        max_turn_rate: float,
        world_width: int,
        world_height: int,
    ) -> None:
        self.position = position
        self.speed = speed
        self.max_turn_rate = max_turn_rate

        self.world_width = world_width
        self.world_height = world_height

        # Start in a random direction.
        angle = random.uniform(0, 2 * math.pi)

        self.velocity = pygame.Vector2(
            math.cos(angle),
            math.sin(angle),
        )

    def update(self, dt: float) -> None:
        """
        Update the fish's movement for one simulation step.
        """

        # Randomly change direction, but only within our
        # maximum allowed turn rate.
        turn_amount = random.uniform(
            -self.max_turn_rate,
            self.max_turn_rate,
        ) * dt

        self.velocity = self.velocity.rotate_rad(turn_amount)

        # Ensure the velocity remains normalized.
        if self.velocity.length_squared() > 0:
            self.velocity = self.velocity.normalize()

        # Move according to velocity * time.
        displacement = self.velocity * self.speed * dt
        self.position += displacement

        # Wrap around world boundaries.
        self._wrap_position()

    def _wrap_position(self) -> None:
        self.position.x %= self.world_width
        self.position.y %= self.world_height