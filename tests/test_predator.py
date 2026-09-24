import pygame

from schoolmind.simulation.config import (
    SimulationConfig,
)
from schoolmind.simulation.predator import Predator
from schoolmind.simulation.world import World


def make_predator(
    capture_cooldown: float = 1.5,
) -> Predator:
    return Predator(
        predator_id=0,
        position=pygame.Vector2(
            500.0,
            350.0,
        ),
        max_speed=170.0,
        max_acceleration=400.0,
        detection_range=250.0,
        capture_radius=12.0,
        capture_cooldown=capture_cooldown,
        world_width=1000,
        world_height=700,
        boundary_margin=0.0,
    )


def test_predator_can_capture_when_cooldown_is_zero() -> None:
    predator = make_predator()

    assert predator.capture_cooldown_remaining == 0.0
    assert predator.can_capture()


def test_capture_starts_cooldown() -> None:
    predator = make_predator(
        capture_cooldown=1.5
    )

    predator.register_capture()

    assert (
        predator.capture_cooldown_remaining
        == 1.5
    )

    assert not predator.can_capture()


def test_capture_cooldown_decreases_over_time() -> None:
    predator = make_predator(
        capture_cooldown=1.5
    )

    predator.register_capture()

    predator.update_capture_cooldown(
        0.5
    )

    assert (
        predator.capture_cooldown_remaining
        == 1.0
    )

    predator.update_capture_cooldown(
        1.0
    )

    assert (
        predator.capture_cooldown_remaining
        == 0.0
    )

    assert predator.can_capture()


def test_capture_cooldown_never_becomes_negative() -> None:
    predator = make_predator(
        capture_cooldown=1.5
    )

    predator.register_capture()

    predator.update_capture_cooldown(
        10.0
    )

    assert (
        predator.capture_cooldown_remaining
        == 0.0
    )

    assert predator.can_capture()


def test_predator_cannot_capture_twice_during_cooldown() -> None:
    config = SimulationConfig(
        width=1000,
        height=700,
        fish_count=2,
        predator_count=1,
        predator_capture_cooldown=1.5,
    )

    world = World(
        config,
        seed=42,
    )

    predator = world.predators[0]

    fish_a = world.fish[0]
    fish_b = world.fish[1]

    predator.position = fish_a.position.copy()

    world._handle_captures()

    assert world.fish_captured == 1
    assert len(world.fish) == 1
    assert (
        predator.capture_cooldown_remaining
        == 1.5
    )

    remaining_fish = world.fish[0]

    predator.position = (
        remaining_fish.position.copy()
    )

    world._handle_captures()

    assert world.fish_captured == 1
    assert len(world.fish) == 1
    assert (
        remaining_fish in world.fish
    )


def test_predator_can_capture_again_after_cooldown() -> None:
    config = SimulationConfig(
        width=1000,
        height=700,
        fish_count=2,
        predator_count=1,
        predator_capture_cooldown=1.5,
    )

    world = World(
        config,
        seed=42,
    )

    predator = world.predators[0]

    fish_a = world.fish[0]
    predator.position = fish_a.position.copy()

    world._handle_captures()

    assert world.fish_captured == 1

    predator.update_capture_cooldown(
        1.5
    )

    remaining_fish = world.fish[0]
    predator.position = (
        remaining_fish.position.copy()
    )

    world._handle_captures()

    assert world.fish_captured == 2
    assert len(world.fish) == 0