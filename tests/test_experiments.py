from pathlib import Path

import yaml

from schoolmind.experiments.config import (
    ExperimentConfig,
    ExperimentSettings,
    load_experiment_config,
)
from schoolmind.experiments.runner import (
    get_trial_seed,
    run_batch,
    run_trial,
)
from schoolmind.experiments.results import (
    write_results,
)
from schoolmind.simulation.config import (
    SimulationConfig,
)
from schoolmind.simulation.world import World


def make_test_config() -> ExperimentConfig:
    return ExperimentConfig(
        experiment=ExperimentSettings(
            name="test",
            random_seed=42,
            simulation_duration=1.0,
            trials=3,
        ),
        simulation=SimulationConfig(
            fish_count=20,
            predator_count=2,
            predator_spawn_pattern="ring",
            predator_coordination_mode="coordinated",
        ),
    )


def test_same_seed_produces_same_trial() -> None:
    config = make_test_config()

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


def test_different_seeds_change_initial_simulation() -> None:
    config = SimulationConfig(
        fish_count=10,
        predator_count=2,
    )

    world_a = World(
        config,
        seed=1,
    )

    world_b = World(
        config,
        seed=2,
    )

    positions_a = [
        fish.position
        for fish in world_a.fish
    ]

    positions_b = [
        fish.position
        for fish in world_b.fish
    ]

    assert positions_a != positions_b


def test_trial_seeds_are_deterministic() -> None:
    assert get_trial_seed(42, 1) == 42
    assert get_trial_seed(42, 2) == 43
    assert get_trial_seed(42, 3) == 44
    assert get_trial_seed(100, 1) == 100


def test_batch_runs_expected_number_of_trials() -> None:
    config = make_test_config()

    results = run_batch(
        config,
        trial_count=3,
    )

    assert len(results) == 3

    assert [
        result["seed"]
        for result in results
    ] == [42, 43, 44]

    assert [
        result["trial_index"]
        for result in results
    ] == [1, 2, 3]


def test_yaml_config_loads(tmp_path: Path) -> None:
    config_path = (
        tmp_path / "experiment.yaml"
    )

    config_data = {
        "experiment": {
            "name": "test",
            "random_seed": 100,
            "simulation_duration": 5.0,
            "trials": 3,
        },
        "simulation": {
            "fish_count": 20,
            "predator_count": 2,
        },
    }

    with config_path.open(
        "w",
        encoding="utf-8",
    ) as file:
        yaml.safe_dump(
            config_data,
            file,
        )

    config = load_experiment_config(
        config_path
    )

    assert config.experiment.name == "test"
    assert config.experiment.trials == 3
    assert config.simulation.fish_count == 20
    assert config.simulation.predator_count == 2


def test_results_contain_resolved_configuration(
    tmp_path: Path,
) -> None:
    config = make_test_config()

    config_path = (
        tmp_path / "input.yaml"
    )

    config_path.write_text(
        yaml.safe_dump(
            {
                "experiment": {
                    "name": "test",
                    "random_seed": 42,
                    "simulation_duration": 1.0,
                    "trials": 1,
                },
                "simulation": {
                    "fish_count": 20,
                    "predator_count": 2,
                },
            }
        ),
        encoding="utf-8",
    )

    results = run_batch(
        config,
        trial_count=1,
    )

    output_directory = (
        tmp_path / "results"
    )

    write_results(
        output_directory=output_directory,
        experiment_id="test_123",
        config_path=config_path,
        experiment_config=config,
        results=results,
    )

    assert (
        output_directory / "config.yaml"
    ).exists()

    assert (
        output_directory
        / "resolved_config.yaml"
    ).exists()

    assert (
        output_directory / "results.json"
    ).exists()

    assert (
        output_directory / "results.csv"
    ).exists()

    payload = yaml.safe_load(
        (
            output_directory
            / "resolved_config.yaml"
        ).read_text(
            encoding="utf-8"
        )
    )

    assert (
        payload["simulation"]["fish_count"]
        == 20
    )

    # This was omitted from the input YAML,
    # so it should come from SimulationConfig.
    assert (
        payload["simulation"][
            "predator_detection_range"
        ]
        == SimulationConfig.predator_detection_range
    )