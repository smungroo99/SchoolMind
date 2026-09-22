import random

import pygame

from schoolmind.simulation.config import SimulationConfig
from schoolmind.simulation.fish import Fish
from schoolmind.simulation.predator import Predator
from schoolmind.behavior.boids import calculate_desired_direction


class World:
    def __init__(self, config: SimulationConfig) -> None:
        self.config = config

        self.fish: list[Fish] = []
        self.predators: list[Predator] = []

        self.elapsed_time = 0.0
        self.fish_captured = 0
        self.first_capture_time: float | None = None

        self._spawn_fish()
        self._spawn_predators()

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

    def _spawn_predators(self) -> None:
        for predator_id in range(self.config.predator_count):
            position = pygame.Vector2(
                random.uniform(0, self.config.width),
                random.uniform(0, self.config.height),
            )

            predator = Predator(
                predator_id=predator_id,
                position=position,
                max_speed=self.config.predator_max_speed,
                max_acceleration=self.config.predator_max_acceleration,
                detection_range=self.config.predator_detection_range,
                capture_radius=self.config.predator_capture_radius,
                world_width=self.config.width,
                world_height=self.config.height,
            )

            self.predators.append(predator)

    def update(self, dt: float) -> None:
        self.elapsed_time += dt

        fish_desired_directions: list[pygame.Vector2 | None] = []

        # ---------------------------------------------------------
        # 1. Calculate every fish's decision using the current
        #    world state.
        # ---------------------------------------------------------
        for fish in self.fish:
            desired_direction = calculate_desired_direction(
                fish=fish,
                all_fish=self.fish,
                neighbor_radius=self.config.neighbor_radius,
                separation_radius=self.config.separation_radius,
                separation_weight=self.config.separation_weight,
                alignment_weight=self.config.alignment_weight,
                cohesion_weight=self.config.cohesion_weight,
                predators=self.predators,
                predator_detection_range=self.config.predator_detection_range,
                predator_avoidance_weight=self.config.predator_avoidance_weight,
            )

            fish_desired_directions.append(desired_direction)

        # ---------------------------------------------------------
        # 2. Calculate every predator's decision using the same
        #    current world state.
        # ---------------------------------------------------------
        predator_desired_directions: list[pygame.Vector2 | None] = []

        for predator in self.predators:
            predator.choose_target(self.fish)

            desired_direction = predator.get_desired_direction()

            predator_desired_directions.append(desired_direction)

        # ---------------------------------------------------------
        # 3. Apply all fish movement.
        # ---------------------------------------------------------
        for fish, desired_direction in zip(
            self.fish,
            fish_desired_directions,
        ):
            fish.update(
                dt,
                desired_direction,
            )

        # ---------------------------------------------------------
        # 4. Apply all predator movement.
        # ---------------------------------------------------------
        for predator, desired_direction in zip(
            self.predators,
            predator_desired_directions,
        ):
            predator.update(
                dt,
                desired_direction,
            )

        # ---------------------------------------------------------
        # 5. Check whether any predators caught fish.
        # ---------------------------------------------------------
        self._handle_captures()

    def _handle_captures(self) -> None:
        captured_fish: list[Fish] = []

        for predator in self.predators:
            closest_fish = None
            closest_distance = predator.capture_radius

            for fish in self.fish:
                if fish in captured_fish:
                    continue

                distance = predator.position.distance_to(
                    fish.position
                )

                if distance <= closest_distance:
                    closest_distance = distance
                    closest_fish = fish

            if closest_fish is not None:
                captured_fish.append(closest_fish)
                predator.target = None

        if not captured_fish:
            return

        self.fish = [
            fish
            for fish in self.fish
            if fish not in captured_fish
        ]

        self.fish_captured += len(captured_fish)

        if self.first_capture_time is None:
            self.first_capture_time = self.elapsed_time

    def get_metrics(self) -> dict:
        return {
            "fish_alive": len(self.fish),
            "fish_captured": self.fish_captured,
            "time_elapsed": self.elapsed_time,
            "time_to_first_capture": self.first_capture_time,
            "active_predators": len(self.predators),
            "predator_target_switches": sum(
                predator.target_switches
                for predator in self.predators
            ),
        }

    def reset(self) -> None:
        self.fish.clear()
        self.predators.clear()

        self.elapsed_time = 0.0
        self.fish_captured = 0
        self.first_capture_time = None

        self._spawn_fish()
        self._spawn_predators()