import pygame

from schoolmind.simulation.config import (
    SimulationConfig,
)
from schoolmind.simulation.fish import Fish
from schoolmind.simulation.predator import Predator
from schoolmind.simulation.world import World


def make_fish(
    position: pygame.Vector2,
    velocity: pygame.Vector2,
) -> Fish:
    fish = Fish(
        fish_id=0,
        position=position,
        target_speed=200.0,
        max_speed=300.0,
        max_acceleration=500.0,
        max_turn_rate=5.0,
        world_width=1000,
        world_height=700,
        radius=5,
        boundary_margin=100.0,
        random_perturbation=False,
    )

    fish.velocity = velocity

    return fish

def make_predator(
    position: pygame.Vector2,
    velocity: pygame.Vector2,
) -> Predator:
    predator = Predator(
        predator_id=0,
        position=position,
        max_speed=300.0,
        max_acceleration=400.0,
        detection_range=250.0,
        capture_radius=12.0,
        capture_cooldown=1.5,
        world_width=1000,
        world_height=700,
        boundary_margin=0.0,
    )

    predator.velocity = velocity
    return predator

def test_fish_does_not_wrap_past_left_boundary() -> None:
    fish = make_fish(
        position=pygame.Vector2(
            5.0,
            350.0,
        ),
        velocity=pygame.Vector2(
            -200.0,
            0.0,
        ),
    )

    fish.update(
        dt=0.1,
        desired_direction=pygame.Vector2(-1, 0),
    )

    assert fish.position.x >= fish.radius
    assert fish.velocity.x >= 0


def test_fish_does_not_wrap_past_right_boundary() -> None:
    fish = make_fish(
        position=pygame.Vector2(
            995.0,
            350.0,
        ),
        velocity=pygame.Vector2(
            200.0,
            0.0,
        ),
    )

    fish.update(
        dt=0.1,
        desired_direction=pygame.Vector2(1, 0),
    )

    assert (
        fish.position.x
        <= fish.world_width - fish.radius
    )

    assert fish.velocity.x <= 0


def test_fish_does_not_wrap_past_top_boundary() -> None:
    fish = make_fish(
        position=pygame.Vector2(
            500.0,
            5.0,
        ),
        velocity=pygame.Vector2(
            0.0,
            -200.0,
        ),
    )

    fish.update(
        dt=0.1,
        desired_direction=pygame.Vector2(0, -1),
    )

    assert fish.position.y >= fish.radius
    assert fish.velocity.y >= 0


def test_fish_does_not_wrap_past_bottom_boundary() -> None:
    fish = make_fish(
        position=pygame.Vector2(
            500.0,
            695.0,
        ),
        velocity=pygame.Vector2(
            0.0,
            200.0,
        ),
    )

    fish.update(
        dt=0.1,
        desired_direction=pygame.Vector2(0, 1),
    )

    assert (
        fish.position.y
        <= fish.world_height - fish.radius
    )

    assert fish.velocity.y <= 0


def test_fish_turns_along_wall_instead_of_reversing() -> None:
    fish = make_fish(
        position=pygame.Vector2(
            995.0,
            350.0,
        ),
        velocity=pygame.Vector2(
            200.0,
            0.0,
        ),
    )

    fish.update(
        dt=0.01,
        desired_direction=pygame.Vector2(1, 0),
    )

    assert (
        fish.position.x
        <= fish.world_width - fish.radius
    )

    assert fish.velocity.y != 0.0


def test_fish_spawn_inside_boundaries() -> None:
    config = SimulationConfig(
        width=1000,
        height=700,
        fish_count=100,
    )

    world = World(
        config,
        seed=42,
    )

    for fish in world.fish:
        assert (
            fish.position.x
            >= config.fish_radius
        )

        assert (
            fish.position.x
            <= config.width - config.fish_radius
        )

        assert (
            fish.position.y
            >= config.fish_radius
        )

        assert (
            fish.position.y
            <= config.height - config.fish_radius
        )


def test_predator_does_not_wrap_past_left_boundary() -> None:
    predator = make_predator(
        position=pygame.Vector2(
            0.0,
            350.0,
        ),
        velocity=pygame.Vector2(
            -200.0,
            0.0,
        ),
    )

    predator.update(
        dt=0.1,
        desired_direction=pygame.Vector2(-1, 0),
    )

    assert predator.position.x >= 0.0
    assert predator.velocity.x >= 0.0


def test_predator_does_not_wrap_past_right_boundary() -> None:
    predator = make_predator(
        position=pygame.Vector2(
            1000.0,
            350.0,
        ),
        velocity=pygame.Vector2(
            200.0,
            0.0,
        ),
    )

    predator.update(
        dt=0.1,
        desired_direction=pygame.Vector2(1, 0),
    )

    assert predator.position.x <= 1000.0
    assert predator.velocity.x <= 0.0


def test_predator_does_not_wrap_past_top_boundary() -> None:
    predator = make_predator(
        position=pygame.Vector2(
            500.0,
            0.0,
        ),
        velocity=pygame.Vector2(
            0.0,
            -200.0,
        ),
    )

    predator.update(
        dt=0.1,
        desired_direction=pygame.Vector2(0, -1),
    )

    assert predator.position.y >= 0.0
    assert predator.velocity.y >= 0.0


def test_predator_does_not_wrap_past_bottom_boundary() -> None:
    predator = make_predator(
        position=pygame.Vector2(
            500.0,
            700.0,
        ),
        velocity=pygame.Vector2(
            0.0,
            200.0,
        ),
    )

    predator.update(
        dt=0.1,
        desired_direction=pygame.Vector2(0, 1),
    )

    assert predator.position.y <= 700.0
    assert predator.velocity.y <= 0.0

def test_predator_can_enter_boundary_margin() -> None:
    predator = make_predator(
        position=pygame.Vector2(
            900.0,
            350.0,
        ),
        velocity=pygame.Vector2(
            200.0,
            0.0,
        ),
    )

    predator.update(
        dt=0.1,
        desired_direction=pygame.Vector2(1, 0),
    )

    # The predator should be allowed to move inside
    # what used to be the 100-pixel exclusion zone.
    assert predator.position.x > 900.0

def test_predator_can_move_through_fish_boundary_margin() -> None:
    predator = make_predator(
        position=pygame.Vector2(
            900.0,
            350.0,
        ),
        velocity=pygame.Vector2(
            200.0,
            0.0,
        ),
    )

    predator.update(
        dt=0.1,
        desired_direction=pygame.Vector2(1, 0),
    )

    assert predator.position.x > 900.0
    assert predator.position.x < 1000.0

def test_predator_bounces_at_actual_right_boundary() -> None:
    predator = make_predator(
        position=pygame.Vector2(
            995.0,
            350.0,
        ),
        velocity=pygame.Vector2(
            200.0,
            0.0,
        ),
    )

    predator.update(
        dt=0.1,
        desired_direction=pygame.Vector2(1, 0),
    )

    assert predator.position.x <= 1000.0
    assert predator.velocity.x <= 0.0