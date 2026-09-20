import math
import random

import pygame


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

    def update(self, dt: float) -> None:
        """Update the fish for one simulation step."""

        # ---------------------------------------------------------
        # 1. Decide what direction we would like to move.
        # ---------------------------------------------------------

        current_direction = self.velocity.normalize()

        if self.random_perturbation:
            turn_amount = random.uniform(
                -self.max_turn_rate,
                self.max_turn_rate,
            ) * dt
        else:
            turn_amount = 0.0

        desired_direction = current_direction.rotate_rad(turn_amount)

        # ---------------------------------------------------------
        # 2. Convert the desired direction into a desired velocity.
        # ---------------------------------------------------------

        desired_velocity = desired_direction * self.target_speed

        # ---------------------------------------------------------
        # 3. Steering is the velocity we want minus
        #    the velocity we currently have.
        # ---------------------------------------------------------

        steering = desired_velocity - self.velocity

        # 4. Convert the desired velocity change into acceleration.
        acceleration = steering / dt

        if acceleration.length_squared() > 0:
            acceleration_length = acceleration.length()

            if acceleration_length > self.max_acceleration:
                acceleration.scale_to_length(self.max_acceleration)

        # ---------------------------------------------------------
        # 5. Update velocity using acceleration.
        # ---------------------------------------------------------

        self.velocity += acceleration * dt

        # ---------------------------------------------------------
        # 6. Prevent velocity from exceeding maximum speed.
        # ---------------------------------------------------------

        if self.velocity.length_squared() > 0:
            if self.velocity.length() > self.max_speed:
                self.velocity.scale_to_length(self.max_speed)

        # ---------------------------------------------------------
        # 7. Update position using velocity.
        # ---------------------------------------------------------

        self.position += self.velocity * dt

        # ---------------------------------------------------------
        # 8. Wrap around world boundaries.
        # ---------------------------------------------------------

        self._wrap_position()

    def _wrap_position(self) -> None:
        self.position.x %= self.world_width
        self.position.y %= self.world_height