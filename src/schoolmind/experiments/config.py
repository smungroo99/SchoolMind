from dataclasses import dataclass, fields
from pathlib import Path
from typing import Any

import yaml

from schoolmind.simulation.config import SimulationConfig


@dataclass(frozen=True)
class ExperimentSettings:
    name: str = "baseline"
    random_seed: int = 42
    simulation_duration: float = 60.0
    trials: int = 10


@dataclass(frozen=True)
class ExperimentConfig:
    experiment: ExperimentSettings
    simulation: SimulationConfig


def _build_dataclass(
    dataclass_type,
    values: dict[str, Any],
):
    allowed_fields = {
        field.name
        for field in fields(dataclass_type)
    }

    unknown_fields = sorted(
        set(values) - allowed_fields
    )

    if unknown_fields:
        raise ValueError(
            f"Unknown fields for {dataclass_type.__name__}: "
            f"{', '.join(unknown_fields)}"
        )

    return dataclass_type(**values)


def load_experiment_config(
    path: str | Path,
) -> ExperimentConfig:
    config_path = Path(path)

    with config_path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    if not isinstance(data, dict):
        raise ValueError(
            "Experiment configuration must contain a YAML mapping."
        )

    allowed_sections = {
        "experiment",
        "simulation",
    }

    unknown_sections = sorted(
        set(data) - allowed_sections
    )

    if unknown_sections:
        raise ValueError(
            "Unknown configuration sections: "
            + ", ".join(unknown_sections)
        )

    experiment_data = data.get("experiment", {})
    simulation_data = data.get("simulation", {})

    if not isinstance(experiment_data, dict):
        raise ValueError(
            "'experiment' must be a YAML mapping."
        )

    if not isinstance(simulation_data, dict):
        raise ValueError(
            "'simulation' must be a YAML mapping."
        )

    experiment = _build_dataclass(
        ExperimentSettings,
        experiment_data,
    )

    simulation = _build_dataclass(
        SimulationConfig,
        simulation_data,
    )

    if experiment.trials <= 0:
        raise ValueError(
            "'trials' must be greater than zero."
        )

    if experiment.simulation_duration <= 0:
        raise ValueError(
            "'simulation_duration' must be greater than zero."
        )

    return ExperimentConfig(
        experiment=experiment,
        simulation=simulation,
    )