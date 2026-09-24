import pygame

from schoolmind.simulation.fish import Fish
from schoolmind.simulation.world import World
from schoolmind.simulation.config import SimulationConfig


def make_fish(
    position: pygame.Vector2,
    velocity: pygame.Vector2,
) -> Fish:
    fish = Fish(
        position=position,
        target_speed=200.0,
        max_speed=300.0,
        max_acceleration=500.0,
        max_turn_rate=5.0,
        world_width=1000,
        world_height=700,
        radius=5,
        boundary_margin=100.0,
        boundary_avoidance_weight=4.0,
        random_perturbation=False,
    )

    fish.velocity = velocity

    return fish


def test_fish_does_not_wrap_past_left_boundary() -> None:
    fish = make_fish(
        position=pygame.Vector2(5.0, 350.0),
        velocity=pygame.Vector2(-200.0, 0.0),
    )

    fish.update(
        dt=0.1,
        desired_direction=pygame.Vector2(-1, 0),
    )

    assert fish.position.x >= fish.radius
    assert fish.velocity.x >= 0


def test_fish_does_not_wrap_past_right_boundary() -> None:
    fish = make_fish(
        position=pygame.Vector2(995.0, 350.0),
        velocity=pygame.Vector2(200.0, 0.0),
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
        position=pygame.Vector2(500.0, 5.0),
        velocity=pygame.Vector2(0.0, -200.0),
    )

    fish.update(
        dt=0.1,
        desired_direction=pygame.Vector2(0, -1),
    )

    assert fish.position.y >= fish.radius
    assert fish.velocity.y >= 0


def test_fish_does_not_wrap_past_bottom_boundary() -> None:
    fish = make_fish(
        position=pygame.Vector2(500.0, 695.0),
        velocity=pygame.Vector2(0.0, 200.0),
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

    def test_fish_turns_along_wall_instead_of_reversing() -> None:
        fish = make_fish(
            position=pygame.Vector2(995.0, 350.0),
            velocity=pygame.Vector2(200.0, 0.0),
        )

        fish.update(
            dt=0.01,
            desired_direction=pygame.Vector2(1, 0),
        )

        assert (
            fish.position.x
            <= fish.world_width - fish.radius
        )

        # Fish should not simply reverse horizontally.
        assert fish.velocity.y != 0.0