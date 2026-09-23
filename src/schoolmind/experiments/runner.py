import argparse
from pathlib import Path

from schoolmind.experiments.config import (
    ExperimentConfig,
    load_experiment_config,
)
from schoolmind.experiments.metrics import (
    calculate_trial_metrics,
    summarize_trials,
)
from schoolmind.experiments.results import (
    create_experiment_id,
    write_results,
)
from schoolmind.simulation.world import World


def get_trial_seed(
    base_seed: int,
    trial_index: int,
) -> int:
    """
    Generate the deterministic seed for a trial.

    Trial 1 uses the base seed, trial 2 uses base seed + 1,
    and so on.
    """
    return base_seed + trial_index - 1


def run_trial(
    experiment_config: ExperimentConfig,
    seed: int,
    trial_index: int,
) -> dict:
    """
    Run one headless simulation trial and return its metrics.
    """
    world = World(
        experiment_config.simulation,
        seed=seed,
    )

    duration = (
        experiment_config
        .experiment
        .simulation_duration
    )

    dt = 1.0 / experiment_config.simulation.fps

    while world.elapsed_time < duration:
        remaining_time = (
            duration - world.elapsed_time
        )

        step_dt = min(
            dt,
            remaining_time,
        )

        world.update(step_dt)

        # Once all fish have been captured,
        # there is no reason to continue the trial.
        if not world.fish:
            break

    return {
        "trial_index": trial_index,
        "seed": seed,
        **calculate_trial_metrics(world),
    }


def run_batch(
    experiment_config: ExperimentConfig,
    trial_count: int | None = None,
) -> list[dict]:
    """
    Run multiple deterministic trials.

    When trial_count is omitted, the value from the
    experiment configuration is used.
    """
    if trial_count is None:
        trial_count = (
            experiment_config
            .experiment
            .trials
        )

    if trial_count <= 0:
        raise ValueError(
            "trial_count must be greater than zero."
        )

    base_seed = (
        experiment_config
        .experiment
        .random_seed
    )

    results = []

    for trial_number in range(
        1,
        trial_count + 1,
    ):
        trial_seed = get_trial_seed(
            base_seed,
            trial_number,
        )

        result = run_trial(
            experiment_config=experiment_config,
            seed=trial_seed,
            trial_index=trial_number,
        )

        results.append(result)

    return results


def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments for the experiment runner.
    """
    parser = argparse.ArgumentParser(
        description=(
            "Run reproducible SchoolMind experiments."
        )
    )

    parser.add_argument(
        "--config",
        required=True,
        help="Path to the experiment YAML file.",
    )

    parser.add_argument(
        "--trials",
        type=int,
        default=None,
        help=(
            "Override the number of trials "
            "defined in the YAML file."
        ),
    )

    parser.add_argument(
        "--output-dir",
        default="runs",
        help=(
            "Directory where experiment results "
            "will be stored."
        ),
    )

    return parser.parse_args()


def main() -> None:
    """
    Execute an experiment from the command line.
    """
    args = parse_args()

    config_path = Path(args.config)

    experiment_config = load_experiment_config(
        config_path
    )

    trial_count = (
        args.trials
        if args.trials is not None
        else experiment_config.experiment.trials
    )

    if trial_count <= 0:
        raise ValueError(
            "--trials must be greater than zero."
        )

    experiment_id = create_experiment_id(
        experiment_config.experiment.name
    )

    results = run_batch(
        experiment_config=experiment_config,
        trial_count=trial_count,
    )

    output_directory = (
        Path(args.output_dir)
        / experiment_id
    )

    write_results(
        output_directory=output_directory,
        experiment_id=experiment_id,
        config_path=config_path,
        experiment_config=experiment_config,
        results=results,
    )

    summary = summarize_trials(results)

    print()
    print("SchoolMind experiment complete")
    print(
        f"Experiment ID: {experiment_id}"
    )
    print(
        f"Trials: {summary['trial_count']}"
    )
    print(
        "Mean survival rate: "
        f"{summary['mean_survival_rate']:.3f}"
    )
    print(
        "Mean capture rate: "
        f"{summary['mean_capture_rate']:.3f}"
    )
    print(
        "Mean time to first capture: "
        f"{summary['mean_time_to_first_capture']}"
    )
    print(
        f"Results: {output_directory}"
    )


if __name__ == "__main__":
    main()
