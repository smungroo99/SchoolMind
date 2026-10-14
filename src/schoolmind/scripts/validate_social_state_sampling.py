
import argparse
import math
from dataclasses import replace
from pathlib import Path

import pygame

from schoolmind.experiments.config import load_experiment_config
from schoolmind.simulation.predation_risk import calculate_capture_risk
from schoolmind.simulation.world import World


SCENARIOS: dict[str, list[tuple[float, float]]] = {
    "isolated": [],
    "dispersed": [
        (75.0, -20.0),
        (75.0, 20.0),
    ],
    "well_grouped": [
        (0.0, -25.0),
        (0.0, 25.0),
        (25.0, -25.0),
        (25.0, 25.0),
    ],
    "overcrowded": [
        (6.0, 0.0),
        (0.0, 6.0),
        (0.0, -6.0),
        (6.0, 6.0),
    ],
}


def run_scenario(
    name: str,
    neighbor_offsets: list[tuple[float, float]],
    simulation_config,
    base_seed: int,
    trial_count: int,
) -> dict:
    """Run fixed social-state capture checks using World sampling."""
    config = replace(
        simulation_config,
        fish_count=len(neighbor_offsets) + 1,
    )

    target_x = 500.0
    target_y = 350.0
    dt = 1.0 / config.fps
    attempts: list[dict] = []

    for trial_index in range(trial_count):
        world = World(
            config,
            seed=base_seed + trial_index,
        )

        if not world.predators:
            raise RuntimeError(
                "This experiment requires at least one predator."
            )

        target = world.fish[0]
        target.position = pygame.Vector2(
            target_x,
            target_y,
        )
        target.velocity = pygame.Vector2(100.0, 0.0)

        for fish, (offset_x, offset_y) in zip(
            world.fish[1:],
            neighbor_offsets,
        ):
            fish.position = pygame.Vector2(
                target_x + offset_x,
                target_y + offset_y,
            )
            fish.velocity = pygame.Vector2(100.0, 0.0)

        predator = world.predators[0]
        predator.position = pygame.Vector2(
            target_x - 10.0,
            target_y,
        )

        predicted = calculate_capture_risk(
            target=target,
            predator=predator,
            all_fish=world.fish,
            config=config,
            dt=dt,
        )

        # Run the actual production capture sampling path.
        world._handle_captures()

        if len(world.capture_attempts) != 1:
            raise RuntimeError(
                f"{name}, trial {trial_index + 1}: expected "
                "one capture attempt, got "
                f"{len(world.capture_attempts)}."
            )

        attempt = world.capture_attempts[0]

        if attempt["fish_id"] != target.fish_id:
            raise RuntimeError(
                f"{name}, trial {trial_index + 1}: "
                "the intended target was not selected."
            )

        if not math.isclose(
            attempt["capture_probability"],
            predicted["capture_probability"],
            rel_tol=1e-12,
            abs_tol=1e-12,
        ):
            raise RuntimeError(
                f"{name}, trial {trial_index + 1}: predicted "
                "and logged probabilities differ."
            )

        attempts.append(attempt)

    probabilities = [
        attempt["capture_probability"]
        for attempt in attempts
    ]

    expected_captures = sum(probabilities)
    observed_captures = sum(
        int(attempt["captured"])
        for attempt in attempts
    )
    expected_variance = sum(
        probability * (1.0 - probability)
        for probability in probabilities
    )

    tolerance = 4.0 * math.sqrt(expected_variance)
    sampling_passed = (
        abs(observed_captures - expected_captures)
        <= tolerance
    )

    first_attempt = attempts[0]

    return {
        "name": name,
        "trials": trial_count,
        "observed_captures": observed_captures,
        "observed_rate": observed_captures / trial_count,
        "expected_captures": expected_captures,
        "expected_rate": expected_captures / trial_count,
        "observed_expected_ratio": (
            observed_captures / expected_captures
            if expected_captures > 0
            else math.nan
        ),
        "tolerance": tolerance,
        "sampling_passed": sampling_passed,
        "risk": {
            metric: first_attempt[metric]
            for metric in (
                "exposure",
                "dispersion",
                "cohesion",
                "dilution",
                "confusion",
                "crowding",
                "capture_hazard",
                "capture_probability",
            )
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Validate predicted and observed capture rates "
            "for controlled social configurations."
        )
    )
    parser.add_argument(
        "--config",
        default="configs/iteration7.yaml",
        help="Experiment configuration YAML.",
    )
    parser.add_argument(
        "--trials",
        type=int,
        default=2000,
        help="Trials per social configuration.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.trials <= 0:
        raise ValueError(
            "--trials must be greater than zero."
        )

    experiment_config = load_experiment_config(
        Path(args.config)
    )
    simulation_config = experiment_config.simulation
    base_seed = experiment_config.experiment.random_seed

    print("Controlled social-state capture validation")
    print(f"Config: {args.config}")
    print(f"Base seed: {base_seed}")
    print(f"Trials per scenario: {args.trials}")
    print("Boids movement is not advanced during these checks.")
    print()

    results = []

    for name, offsets in SCENARIOS.items():
        result = run_scenario(
            name=name,
            neighbor_offsets=offsets,
            simulation_config=simulation_config,
            base_seed=base_seed,
            trial_count=args.trials,
        )
        results.append(result)
        risk = result["risk"]

        print(f"Scenario: {name}")
        print(f"  Neighbors:             {len(offsets)}")
        print(f"  Exposure:              {risk['exposure']:.4f}")
        print(f"  Dispersion:            {risk['dispersion']:.4f}")
        print(f"  Cohesion:              {risk['cohesion']:.4f}")
        print(f"  Dilution:              {risk['dilution']:.4f}")
        print(f"  Confusion:             {risk['confusion']:.4f}")
        print(f"  Crowding:              {risk['crowding']:.4f}")
        print(f"  Capture hazard:        {risk['capture_hazard']:.5f}")
        print(f"  Predicted probability: {risk['capture_probability']:.6f}")
        print(f"  Expected captures:     {result['expected_captures']:.2f}")
        print(f"  Observed captures:     {result['observed_captures']}")
        print(f"  Observed rate:         {result['observed_rate']:.5f}")
        print(f"  Observed/expected:     {result['observed_expected_ratio']:.3f}")
        print(
            "  Within 4 SD:           "
            f"{'PASS' if result['sampling_passed'] else 'FAIL'}"
        )
        print()

    by_name = {
        result["name"]: result
        for result in results
    }
    hazards = {
        name: result["risk"]["capture_hazard"]
        for name, result in by_name.items()
    }

    print("Combined social-state comparisons")
    print(
        "  Isolated > dispersed > well-grouped: "
        f"{hazards['isolated'] > hazards['dispersed'] > hazards['well_grouped']}"
    )
    print(
        "  Overcrowded > well-grouped: "
        f"{hazards['overcrowded'] > hazards['well_grouped']}"
    )

    if not all(
        result["sampling_passed"]
        for result in results
    ):
        raise SystemExit(
            "FAIL: at least one observed capture count fell "
            "outside its four-standard-deviation tolerance."
        )


if __name__ == "__main__":
    main()