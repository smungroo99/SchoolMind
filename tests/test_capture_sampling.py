
import math

import pygame

from schoolmind.simulation.config import SimulationConfig
from schoolmind.simulation.world import World


def test_observed_captures_match_predicted_probabilities() -> None:
    trial_count = 2_000

    config = SimulationConfig(
        fish_count=1,
        predator_count=1,
        predation_baseline_hazard=5.0,
        random_perturbation=False,
    )

    observed_captures = 0
    expected_captures = 0.0
    expected_variance = 0.0

    for seed in range(trial_count):
        world = World(
            config,
            seed=seed,
        )

        fish = world.fish[0]
        predator = world.predators[0]

        # Keep the target and predator in a fixed,
        # valid capture configuration for every trial.
        fish.position = pygame.Vector2(
            500.0,
            350.0,
        )
        predator.position = pygame.Vector2(
            510.0,
            350.0,
        )

        world._handle_captures()

        assert len(world.capture_attempts) == 1

        attempt = world.capture_attempts[0]
        probability = attempt["capture_probability"]

        observed_captures += int(
            attempt["captured"]
        )
        expected_captures += probability
        expected_variance += (
            probability * (1.0 - probability)
        )

    # Ensure this configuration produces a meaningful
    # stochastic test rather than probabilities near 0 or 1.
    assert 0.0 < expected_captures < trial_count
    assert expected_variance > 0.0

    # Under independent Bernoulli sampling, the capture
    # count should normally remain within four standard
    # deviations of the model's expected capture count.
    tolerance = 4.0 * math.sqrt(expected_variance)

    assert abs(
        observed_captures - expected_captures
    ) <= tolerance, (
        f"Observed {observed_captures} captures across "
        f"{trial_count} trials, but the model expected "
        f"{expected_captures:.2f} "
        f"(tolerance: {tolerance:.2f})."
    )
