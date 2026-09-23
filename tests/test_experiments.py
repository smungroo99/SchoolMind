from pathlib import Path

import yaml

from schoolmind.experiments.config import (
    load_experiment_config,
)
from schoolmind.experiments.runner import run_trial
from schoolmind.simulation.config import SimulationConfig


def test_same_seed_produces_same_trial() -> None:
    config = SimulationConfig(
        fish_count=20,
        predator_count=2,
        predator_spawn_pattern="ring",
        predator_coordination_mode="coordinated",
    )

    from schoolmind.experiments.config import (
        ExperimentConfig,
        ExperimentSettings,
    )

    experiment_config = ExperimentConfig(
        experiment=ExperimentSettings(
            simulation_duration=1.0,
        ),
        simulation=config,
    )

    first = run_trial(
        experiment_config,
        seed=123,
        trial_index=1,
    )

    second = run_trial(
        experiment_config,
        seed=123,
        trial_index=1,
    )

    assert first == second


def test_different_seeds_change_initial_simulation() -> None:
    config = SimulationConfig(
        fish_count=10,
        predator_count=2,
    )

    from schoolmind.simulation.world import World

    world_a = World(config, seed=1)
    world_b = World(config, seed=2)

    fish_positions_a = [
        fish.position
        for fish in world_a.fish
    ]

    fish_positions_b = [
        fish.position
        for fish in world_b.fish
    ]

    assert fish_positions_a != fish_positions_b


def test_yaml_config_loads(tmp_path: Path) -> None:
    config_path = tmp_path / "experiment.yaml"

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