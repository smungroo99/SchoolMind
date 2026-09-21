import random

import pygame

from schoolmind.simulation.config import SimulationConfig
from schoolmind.simulation.fish import Fish
from schoolmind.behavior.boids import calculate_desired_direction

class World:
    def __init__(self, config: SimulationConfig) -> None:
        self.config = config
        self.fish: list[Fish] = []

        self._spawn_fish()

    def _spawn_fish(self) -> None:
        for _ in range(self.config.fish_count):
            position = pygame.Vector2(
                random.uniform(0, self.config.width),
                random.uniform(0, self.config.height),
            )

            target_speed = random.uniform(
                self.config.min_fish_speed,
                self.config.max_fish_speed,
            )

            fish = Fish(
                position=position,
                target_speed=target_speed,
                max_speed=self.config.max_fish_speed,
                max_acceleration=self.config.max_fish_acceleration,
                max_turn_rate=self.config.max_turn_rate,
                world_width=self.config.width,
                world_height=self.config.height,
                random_perturbation=self.config.random_perturbation,
            )

            self.fish.append(fish)

    def update(self, dt: float) -> None:
        desired_directions: list[pygame.Vector2 | None] = []

        # First calculate every fish's decision using
        # the current world state.
        for fish in self.fish:
            desired_direction = calculate_desired_direction(
                fish=fish,
                all_fish=self.fish,
                neighbor_radius=self.config.neighbor_radius,
                separation_radius=self.config.separation_radius,
                separation_weight=self.config.separation_weight,
                alignment_weight=self.config.alignment_weight,
                cohesion_weight=self.config.cohesion_weight,
            )

            desired_directions.append(desired_direction)

        # Now update every fish.
        for fish, desired_direction in zip(
            self.fish,
            desired_directions,
        ):
            fish.update(
                dt,
                desired_direction,
            )

    def reset(self) -> None:
        self.fish.clear()
        self._spawn_fish()