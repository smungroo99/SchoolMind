import csv
import json
import re
import shutil
import subprocess
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from importlib.metadata import (
    PackageNotFoundError,
    version,
)
from pathlib import Path

import yaml

from schoolmind.experiments.config import ExperimentConfig
from schoolmind.experiments.metrics import summarize_trials


def create_experiment_id(name: str) -> str:
    """
    Create a filesystem-safe, timestamped experiment ID.

    Microseconds are included so that two experiments started
    in the same second still receive different IDs.
    """
    safe_name = re.sub(
        r"[^a-zA-Z0-9_-]+",
        "_",
        name,
    ).strip("_")

    if not safe_name:
        safe_name = "experiment"

    timestamp = datetime.now(
        timezone.utc
    ).strftime("%Y%m%dT%H%M%S_%fZ")

    return f"{safe_name}_{timestamp}"


def get_git_commit() -> str:
    """
    Return the Git commit corresponding to the code being run.

    Returns "unknown" when the project is not being run from
    a Git repository or Git cannot be queried.
    """
    try:
        repository_path = Path(__file__).resolve()

        for path in repository_path.parents:
            if (path / ".git").exists():
                result = subprocess.run(
                    [
                        "git",
                        "rev-parse",
                        "HEAD",
                    ],
                    cwd=path,
                    capture_output=True,
                    text=True,
                    check=True,
                )

                return result.stdout.strip()

    except (
        OSError,
        subprocess.CalledProcessError,
    ):
        pass

    return "unknown"


def get_schoolmind_version() -> str:
    """
    Return the installed SchoolMind package version.

    Returns "unknown" when the package metadata is unavailable.
    """
    try:
        return version("schoolmind")
    except PackageNotFoundError:
        return "unknown"


def write_results(
    output_directory: Path,
    experiment_id: str,
    config_path: Path,
    experiment_config: ExperimentConfig,
    results: list[dict],
) -> None:
    """
    Persist all outputs associated with an experiment.

    Files written:

    - config.yaml
        The exact configuration supplied by the user.

    - resolved_config.yaml
        The complete configuration after SimulationConfig
        defaults have been applied.

    - results.json
        Experiment metadata, configuration, trial results,
        and summary statistics.

    - results.csv
        Flat trial-level results suitable for pandas/data analysis.
    """
    if output_directory.exists():
        raise FileExistsError(
            "Experiment output already exists: "
            f"{output_directory}"
        )

    output_directory.mkdir(
        parents=True,
        exist_ok=False,
    )

    # ------------------------------------------------------------------
    # Configuration
    # ------------------------------------------------------------------

    # Preserve the exact YAML supplied by the user.
    shutil.copyfile(
        config_path,
        output_directory / "config.yaml",
    )

    # Save the fully resolved configuration.
    #
    # ExperimentConfig contains all values after the YAML has been
    # loaded into the dataclasses, meaning omitted simulation values
    # have already received their SimulationConfig defaults.
    resolved_config = {
        "experiment": asdict(
            experiment_config.experiment
        ),
        "simulation": asdict(
            experiment_config.simulation
        ),
    }

    with (
        output_directory / "resolved_config.yaml"
    ).open(
        "w",
        encoding="utf-8",
    ) as file:
        yaml.safe_dump(
            resolved_config,
            file,
            sort_keys=False,
        )

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------

    summary = summarize_trials(results)

    # ------------------------------------------------------------------
    # Reproducibility metadata
    # ------------------------------------------------------------------

    metadata = {
        "experiment_id": experiment_id,
        "created_at_utc": datetime.now(
            timezone.utc
        ).isoformat(),
        "python_version": sys.version,
        "schoolmind_version": get_schoolmind_version(),
        "git_commit": get_git_commit(),
        "base_seed": (
            experiment_config
            .experiment
            .random_seed
        ),
        "seed_strategy": (
            "trial_seed = "
            "base_seed + trial_index - 1"
        ),
    }

    # ------------------------------------------------------------------
    # JSON
    # ------------------------------------------------------------------

    json_payload = {
        "metadata": metadata,
        "experiment": asdict(
            experiment_config.experiment
        ),
        "simulation": asdict(
            experiment_config.simulation
        ),
        "trials": results,
        "summary": summary,
    }

    with (
        output_directory / "results.json"
    ).open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            json_payload,
            file,
            indent=2,
        )

    # ------------------------------------------------------------------
    # CSV
    # ------------------------------------------------------------------

    csv_fields = [
        "experiment_id",
        "trial_index",
        "seed",
        "fish_initial",
        "fish_alive",
        "fish_captured",
        "survival_rate",
        "capture_rate",
        "time_elapsed",
        "time_to_first_capture",
        "time_to_extinction",
        "predator_count",
        "predator_target_switches",
        "predator_spawn_pattern",
        "predator_coordination_mode",
    ]

    with (
        output_directory / "results.csv"
    ).open(
        "w",
        encoding="utf-8",
        newline="",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=csv_fields,
        )

        writer.writeheader()

        for result in results:
            writer.writerow(
                {
                    "experiment_id": experiment_id,
                    **result,
                }
            )