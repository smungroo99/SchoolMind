
import argparse
from dataclasses import replace
from pathlib import Path

import pygame

from schoolmind.experiments.config import load_experiment_config
from schoolmind.simulation.config import SimulationConfig
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

STRENGTH_VALUES = (0.0, 0.25, 0.5, 1.0, 2.0)


def calculate_scenario_risk(
    offsets: list[tuple[float, float]],
    base_config: SimulationConfig,
    seed: int,
    dispersion_strength: float,
    cohesion_strength: float,
) -> dict:
    """Calculate deterministic risk for a fixed social configuration."""
    config = replace(
        base_config,
        fish_count=len(offsets) + 1,
        predation_dispersion_strength=dispersion_strength,
        predation_cohesion_strength=cohesion_strength,
    )

    target_x = 500.0
    target_y = 350.0

    world = World(config, seed=seed)

    target = world.fish[0]
    target.position = pygame.Vector2(target_x, target_y)
    target.velocity = pygame.Vector2(100.0, 0.0)

    for fish, (offset_x, offset_y) in zip(
        world.fish[1:],
        offsets,
    ):
        fish.position = pygame.Vector2(
            target_x + offset_x,
            target_y + offset_y,
        )
        fish.velocity = pygame.Vector2(100.0, 0.0)

    # Keep predator position and distance identical across scenarios.
    predator = world.predators[0]
    predator.position = pygame.Vector2(
        target_x - 10.0,
        target_y,
    )

    return calculate_capture_risk(
        target=target,
        predator=predator,
        all_fish=world.fish,
        config=config,
        dt=1.0 / config.fps,
    )


def calculate_all_scenarios(
    base_config: SimulationConfig,
    seed: int,
    dispersion_strength: float,
    cohesion_strength: float,
) -> dict[str, dict]:
    return {
        name: calculate_scenario_risk(
            offsets=offsets,
            base_config=base_config,
            seed=seed,
            dispersion_strength=dispersion_strength,
            cohesion_strength=cohesion_strength,
        )
        for name, offsets in SCENARIOS.items()
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Analyze capture-risk sensitivity to dispersion "
            "and cohesion strengths."
        )
    )
    parser.add_argument(
        "--config",
        default="configs/iteration7.yaml",
        help="Configuration used for all other risk parameters.",
    )
    args = parser.parse_args()

    experiment_config = load_experiment_config(
        Path(args.config)
    )
    base_config = experiment_config.simulation
    seed = experiment_config.experiment.random_seed

    print("Dispersion/cohesion sensitivity analysis")
    print(f"Config: {args.config}")
    print(f"Seed: {seed}")
    print(f"Strength values: {STRENGTH_VALUES}")
    print("No movement updates or random capture sampling are performed.")
    print()

    print(
        "Disp Coh | Isolated  Dispersed  Grouped  Overcrowded"
        " | Iso/Group  Crowd/Group | Risk ranking (high to low)"
    )
    print("-" * 116)

    for dispersion_strength in STRENGTH_VALUES:
        for cohesion_strength in STRENGTH_VALUES:
            results = calculate_all_scenarios(
                base_config=base_config,
                seed=seed,
                dispersion_strength=dispersion_strength,
                cohesion_strength=cohesion_strength,
            )

            hazards = {
                name: results[name]["capture_hazard"]
                for name in SCENARIOS
            }

            ratio_isolated_grouped = (
                hazards["isolated"]
                / hazards["well_grouped"]
            )
            ratio_crowded_grouped = (
                hazards["overcrowded"]
                / hazards["well_grouped"]
            )

            ranking = sorted(
                hazards,
                key=hazards.__getitem__,
                reverse=True,
            )

            ranking_text = " > ".join(
                {
                    "isolated": "ISO",
                    "dispersed": "DISP",
                    "well_grouped": "GROUP",
                    "overcrowded": "CROWD",
                }[name]
                for name in ranking
            )

            print(
                f"{dispersion_strength:4.2f} "
                f"{cohesion_strength:4.2f} | "
                f"{hazards['isolated']:8.3f} "
                f"{hazards['dispersed']:10.3f} "
                f"{hazards['well_grouped']:8.3f} "
                f"{hazards['overcrowded']:11.3f} | "
                f"{ratio_isolated_grouped:9.3f} "
                f"{ratio_crowded_grouped:11.3f} | "
                f"{ranking_text}"
            )

    print()
    print("Interpretation:")
    print("  ISO/GROUP: how many times higher isolated-fish hazard is")
    print("             than well-grouped-fish hazard.")
    print("  CROWD/GROUP: how many times higher overcrowded-fish hazard is")
    print("               than well-grouped-fish hazard.")
    print("  DISP = dispersed, GROUP = well-grouped.")
    print("  Strengths are modeling coefficients, not measured biology.")


if __name__ == "__main__":
    main()