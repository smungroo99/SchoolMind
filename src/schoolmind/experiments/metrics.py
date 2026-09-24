from statistics import mean, stdev
from typing import Any

from schoolmind.simulation.world import World

def calculate_trial_metrics(
    world: World,
) -> dict[str, Any]:
    metrics = world.get_metrics()

    initial_fish = world.initial_fish_count

    if initial_fish > 0:
        survival_rate = (
            metrics["fish_alive"]
            / initial_fish
        )

        capture_rate = (
            metrics["fish_captured"]
            / initial_fish
        )
    else:
        survival_rate = 0.0
        capture_rate = 0.0

    return {
        "fish_initial": initial_fish,
        "fish_alive": metrics["fish_alive"],
        "fish_captured": metrics["fish_captured"],
        "survival_rate": survival_rate,
        "capture_rate": capture_rate,
        "time_elapsed": metrics["time_elapsed"],
        "time_to_first_capture": (
            metrics["time_to_first_capture"]
        ),
        "time_to_extinction": (
            metrics["time_to_extinction"]
        ),
        "predator_count": metrics["predator_count"],
        "predator_target_switches": (
            metrics["predator_target_switches"]
        ),
        "predator_spawn_pattern": (
            world.config.predator_spawn_pattern
        ),
        "predator_coordination_mode": (
            world.config.predator_coordination_mode
        ),
    }

def summarize_trials(
    trials: list[dict[str, Any]],
) -> dict[str, Any]:
    if not trials:
        raise ValueError(
            "Cannot summarize an empty trial set."
        )

    survival_rates = [
        trial["survival_rate"]
        for trial in trials
    ]

    capture_rates = [
        trial["capture_rate"]
        for trial in trials
    ]

    fish_captured = [
        trial["fish_captured"]
        for trial in trials
    ]

    first_capture_times = [
        trial["time_to_first_capture"]
        for trial in trials
        if trial["time_to_first_capture"] is not None
    ]

    extinction_times = [
        trial["time_to_extinction"]
        for trial in trials
        if trial["time_to_extinction"] is not None
    ]

    return {
        "trial_count": len(trials),

        "mean_survival_rate": mean(
            survival_rates
        ),
        "std_survival_rate": (
            stdev(survival_rates)
            if len(survival_rates) > 1
            else 0.0
        ),

        "mean_capture_rate": mean(
            capture_rates
        ),

        "mean_fish_captured": mean(
            fish_captured
        ),

        "capture_trials": len(
            first_capture_times
        ),
        "no_capture_trials": (
            len(trials)
            - len(first_capture_times)
        ),

        "mean_time_to_first_capture": (
            mean(first_capture_times)
            if first_capture_times
            else None
        ),

        "extinction_trials": len(
            extinction_times
        ),

        "mean_time_to_extinction": (
            mean(extinction_times)
            if extinction_times
            else None
        ),
    }