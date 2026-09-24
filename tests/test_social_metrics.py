from pathlib import Path

import yaml

from schoolmind.experiments.config import (
    ExperimentConfig,
    ExperimentSettings,
)
from schoolmind.experiments.results import (
    write_results,
)
from schoolmind.experiments.runner import (
    run_trial,
)
from schoolmind.experiments.social_metrics import (
    calculate_fish_social_state,
    calculate_school_social_metrics,
    collect_individual_social_snapshot,
)

from schoolmind.simulation.config import (
    SimulationConfig,
)
from schoolmind.simulation.world import World


def make_world() -> World:
    config = SimulationConfig(
        width=1000,
        height=700,
        fish_count=3,
        predator_count=0,
        random_perturbation=False,
    )

    world = World(
        config,
        seed=42,
    )

    world.fish[0].position = (
        world.fish[0].position.copy()
    )
    world.fish[0].position.x = 100.0
    world.fish[0].position.y = 100.0

    world.fish[1].position = (
        world.fish[1].position.copy()
    )
    world.fish[1].position.x = 110.0
    world.fish[1].position.y = 100.0

    world.fish[2].position = (
        world.fish[2].position.copy()
    )
    world.fish[2].position.x = 90.0
    world.fish[2].position.y = 100.0

    for fish in world.fish:
        fish.velocity.x = 1.0
        fish.velocity.y = 0.0

    return world


def test_fish_social_state() -> None:
    world = make_world()

    state = calculate_fish_social_state(
        fish=world.fish[0],
        all_fish=world.fish,
        neighbor_radius=100.0,
    )

    assert state["neighbor_count"] == 2
    assert (
        state["nearest_neighbor_distance"]
        == 10.0
    )
    assert (
        state["mean_neighbor_distance"]
        == 10.0
    )
    assert state["alignment"] == 1.0
    assert (
        state["cohesion_distance"]
        == 00.0
    )


def test_school_social_metrics() -> None:
    world = make_world()

    metrics = calculate_school_social_metrics(
        world
    )

    assert metrics["fish_count"] == 3
    assert (
        metrics["isolated_fish_fraction"]
        == 0.0
    )
    assert (
        metrics["mean_neighbor_count"]
        == 2.0
    )
    assert (
        metrics["mean_nearest_neighbor_distance"]
        == 10.0
    )
    assert (
        metrics["mean_alignment"]
        == 1.0
    )
    assert (
        metrics["polarization"]
        == 1.0
    )
    assert metrics["dispersion"] > 0.0


def test_isolated_fish_is_detected() -> None:
    world = make_world()

    world.fish[0].position.x = 500.0

    metrics = calculate_school_social_metrics(
        world
    )

    assert (
        metrics["isolated_fish_fraction"]
        == 1.0 / 3.0
    )


def test_social_metrics_are_deterministic() -> None:
    config = ExperimentConfig(
        experiment=ExperimentSettings(
            name="social_test",
            random_seed=42,
            simulation_duration=1.0,
            trials=1,
            metrics_sample_interval=0.5,
        ),
        simulation=SimulationConfig(
            fish_count=10,
            predator_count=1,
        ),
    )

    first = run_trial(
        config,
        seed=123,
        trial_index=1,
    )

    second = run_trial(
        config,
        seed=123,
        trial_index=1,
    )

    assert first == second


def test_social_metrics_are_recorded_over_time() -> None:
    config = ExperimentConfig(
        experiment=ExperimentSettings(
            name="social_test",
            random_seed=42,
            simulation_duration=1.0,
            trials=1,
            metrics_sample_interval=0.5,
        ),
        simulation=SimulationConfig(
            fish_count=10,
            predator_count=0,
        ),
    )

    result = run_trial(
        config,
        seed=123,
        trial_index=1,
    )

    snapshots = result[
        "social_time_series"
    ]

    assert len(snapshots) >= 2
    assert snapshots[0]["time"] == 0.0

    assert snapshots[0]["fish_count"] == 10

    assert all(
        "mean_alignment" in snapshot
        for snapshot in snapshots
    )


def test_social_metrics_csv_is_written(
    tmp_path: Path,
) -> None:
    config = ExperimentConfig(
        experiment=ExperimentSettings(
            name="social_test",
            random_seed=42,
            simulation_duration=1.0,
            trials=1,
            metrics_sample_interval=0.5,
        ),
        simulation=SimulationConfig(
            fish_count=10,
            predator_count=0,
        ),
    )

    config_path = (
        tmp_path / "experiment.yaml"
    )

    config_path.write_text(
        yaml.safe_dump(
            {
                "experiment": {
                    "name": "social_test",
                    "random_seed": 42,
                    "simulation_duration": 1.0,
                    "trials": 1,
                    "metrics_sample_interval": 0.5,
                },
                "simulation": {
                    "fish_count": 10,
                    "predator_count": 0,
                },
            }
        ),
        encoding="utf-8",
    )

    result = run_trial(
        config,
        seed=42,
        trial_index=1,
    )

    output_directory = (
        tmp_path / "results"
    )

    write_results(
        output_directory=output_directory,
        experiment_id="social_test_123",
        config_path=config_path,
        experiment_config=config,
        results=[result],
    )

    social_metrics_path = (
        output_directory
        / "social_metrics.csv"
    )

    assert social_metrics_path.exists()

    contents = social_metrics_path.read_text(
        encoding="utf-8"
    )

    assert (
        "isolated_fish_fraction"
        in contents
    )

    assert (
        "mean_alignment"
        in contents
    )

    assert (
        "polarization"
        in contents
    )

def test_individual_social_snapshot() -> None:
    world = make_world()

    snapshots = (
        collect_individual_social_snapshot(
            world
        )
    )

    assert len(snapshots) == 3

    assert {
        snapshot["fish_id"]
        for snapshot in snapshots
    } == {0, 1, 2}

    assert all(
        snapshot["time"] == 0.0
        for snapshot in snapshots
    )

    assert all(
        "neighbor_count" in snapshot
        for snapshot in snapshots
    )

    assert all(
        "alignment" in snapshot
        for snapshot in snapshots
    )

    assert all(
        "cohesion_distance" in snapshot
        for snapshot in snapshots
    )

def test_capture_events_record_fish_and_predator() -> None:
    config = SimulationConfig(
        fish_count=1,
        predator_count=1,
    )

    world = World(
        config,
        seed=42,
    )

    fish = world.fish[0]
    predator = world.predators[0]

    predator.position = fish.position.copy()

    world._handle_captures()

    assert len(world.capture_events) == 1

    event = world.capture_events[0]

    assert event["fish_id"] == fish.fish_id
    assert event["predator_id"] == predator.id
    assert event["time"] == world.elapsed_time