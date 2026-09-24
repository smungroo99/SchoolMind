from statistics import mean
from typing import Any

import pygame

from schoolmind.behavior.boids import get_neighbors
from schoolmind.simulation.fish import Fish
from schoolmind.simulation.world import World


def _mean_or_none(
    values: list[float],
) -> float | None:
    if not values:
        return None

    return mean(values)


def _calculate_polarization(
    fish: list[Fish],
) -> float | None:
    """
    Calculate directional coherence for a group of fish.

    Returns a value in [0, 1].

    A value near 1 means fish are moving in the same direction.
    A value near 0 means their directions cancel or are highly mixed.
    """
    if len(fish) < 2:
        return None

    direction_sum = pygame.Vector2()
    moving_fish_count = 0

    for current_fish in fish:
        if (
            current_fish.velocity.length_squared()
            == 0
        ):
            continue

        direction_sum += (
            current_fish.velocity.normalize()
        )

        moving_fish_count += 1

    if moving_fish_count == 0:
        return None

    return (
        direction_sum.length()
        / moving_fish_count
    )


def _calculate_dispersion(
    fish: list[Fish],
) -> float | None:
    """
    Calculate the mean distance of fish from
    their group's centroid.
    """
    if len(fish) < 2:
        return None

    centroid = pygame.Vector2()

    for current_fish in fish:
        centroid += current_fish.position

    centroid /= len(fish)

    distances = [
        current_fish.position.distance_to(
            centroid
        )
        for current_fish in fish
    ]

    return mean(distances)


def _find_clusters(
    fish: list[Fish],
    neighbor_radius: float,
) -> list[list[Fish]]:
    """
    Find connected components in the fish neighborhood graph.

    Two fish are directly connected when they are within
    neighbor_radius of each other.

    Indirect connections are allowed:

        A -- B -- C

    A and C can therefore belong to the same cluster even if
    they are farther apart than neighbor_radius.

    Clusters are returned in deterministic order by their
    smallest fish ID.
    """
    remaining = set(fish)
    clusters: list[list[Fish]] = []

    while remaining:
        start = min(
            remaining,
            key=lambda current_fish: current_fish.fish_id,
        )

        remaining.remove(start)

        queue = [start]
        cluster: list[Fish] = []

        while queue:
            current_fish = queue.pop()
            cluster.append(current_fish)

            neighbors = get_neighbors(
                fish=current_fish,
                all_fish=fish,
                neighbor_radius=neighbor_radius,
            )

            for neighbor in neighbors:
                if neighbor in remaining:
                    remaining.remove(neighbor)
                    queue.append(neighbor)

        cluster.sort(
            key=lambda current_fish: current_fish.fish_id
        )

        clusters.append(cluster)

    clusters.sort(
        key=lambda cluster: cluster[0].fish_id
    )

    return clusters


def calculate_fish_social_state(
    fish: Fish,
    all_fish: list[Fish],
    neighbor_radius: float,
) -> dict[str, Any]:
    """
    Calculate the local social state of one fish.

    These measurements are observational only.
    They do not affect fish behavior.
    """
    neighbors = get_neighbors(
        fish=fish,
        all_fish=all_fish,
        neighbor_radius=neighbor_radius,
    )

    neighbor_count = len(neighbors)

    if not neighbors:
        return {
            "neighbor_count": 0,
            "nearest_neighbor_distance": None,
            "mean_neighbor_distance": None,
            "alignment": None,
            "cohesion_distance": None,
        }

    distances = [
        fish.position.distance_to(
            neighbor.position
        )
        for neighbor in neighbors
    ]

    nearest_neighbor_distance = min(
        distances
    )

    mean_neighbor_distance = mean(
        distances
    )

    alignment_scores: list[float] = []

    if fish.velocity.length_squared() > 0:
        fish_direction = (
            fish.velocity.normalize()
        )

        for neighbor in neighbors:
            if (
                neighbor.velocity.length_squared()
                == 0
            ):
                continue

            neighbor_direction = (
                neighbor.velocity.normalize()
            )

            cosine_similarity = (
                fish_direction.dot(
                    neighbor_direction
                )
            )

            alignment_score = (
                cosine_similarity + 1.0
            ) / 2.0

            alignment_scores.append(
                alignment_score
            )

    alignment = _mean_or_none(
        alignment_scores
    )

    local_center = pygame.Vector2()

    for neighbor in neighbors:
        local_center += neighbor.position

    local_center /= len(neighbors)

    cohesion_distance = (
        fish.position.distance_to(
            local_center
        )
    )

    return {
        "neighbor_count": neighbor_count,
        "nearest_neighbor_distance": (
            nearest_neighbor_distance
        ),
        "mean_neighbor_distance": (
            mean_neighbor_distance
        ),
        "alignment": alignment,
        "cohesion_distance": (
            cohesion_distance
        ),
    }


def _calculate_cluster_metrics(
    clusters: list[list[Fish]],
    all_fish: list[Fish],
    neighbor_radius: float,
) -> list[dict[str, Any]]:
    """
    Calculate metrics for each connected cluster.

    Singleton clusters are retained because they represent
    locally isolated fish.

    cluster_id is the smallest fish ID in the cluster.
    It identifies a cluster within a snapshot only and is
    not intended to persist across time.
    """
    cluster_metrics: list[dict[str, Any]] = []

    for cluster in clusters:
        cluster_states = [
            calculate_fish_social_state(
                fish=current_fish,
                all_fish=cluster,
                neighbor_radius=neighbor_radius,
            )
            for current_fish in cluster
        ]

        alignments = [
            state["alignment"]
            for state in cluster_states
            if state["alignment"] is not None
        ]

        nearest_neighbor_distances = [
            state[
                "nearest_neighbor_distance"
            ]
            for state in cluster_states
            if state[
                "nearest_neighbor_distance"
            ] is not None
        ]

        mean_neighbor_distances = [
            state["mean_neighbor_distance"]
            for state in cluster_states
            if state[
                "mean_neighbor_distance"
            ] is not None
        ]

        cohesion_distances = [
            state["cohesion_distance"]
            for state in cluster_states
            if state[
                "cohesion_distance"
            ] is not None
        ]

        cluster_metrics.append(
            {
                "cluster_id": (
                    cluster[0].fish_id
                ),
                "cluster_size": len(cluster),
                "fish_fraction": (
                    len(cluster)
                    / len(all_fish)
                ),
                "mean_alignment": (
                    _mean_or_none(
                        alignments
                    )
                ),
                "mean_nearest_neighbor_distance": (
                    _mean_or_none(
                        nearest_neighbor_distances
                    )
                ),
                "mean_neighbor_distance": (
                    _mean_or_none(
                        mean_neighbor_distances
                    )
                ),
                "mean_cohesion_distance": (
                    _mean_or_none(
                        cohesion_distances
                    )
                ),
                "polarization": (
                    _calculate_polarization(
                        cluster
                    )
                ),
                "dispersion": (
                    _calculate_dispersion(
                        cluster
                    )
                ),
            }
        )

    return cluster_metrics


def calculate_school_social_metrics(
    world: World,
) -> dict[str, Any]:
    """
    Calculate individual-population, global, and
    cluster-level social metrics.
    """
    fish = world.fish

    if not fish:
        return {
            "fish_count": 0,
            "isolated_fish_fraction": 0.0,
            "mean_neighbor_count": None,
            "mean_nearest_neighbor_distance": None,
            "mean_neighbor_distance": None,
            "mean_alignment": None,
            "mean_cohesion_distance": None,
            "global_polarization": None,
            "global_dispersion": None,
            "cluster_count": 0,
            "school_count": 0,
            "school_fish_fraction": 0.0,
            "largest_cluster_size": 0,
            "largest_cluster_fraction": 0.0,
            "mean_cluster_size": None,
            "mean_school_size": None,
            "mean_school_polarization": None,
            "mean_school_dispersion": None,
            "clusters": [],
        }

    neighbor_radius = (
        world.config.neighbor_radius
    )

    states = [
        calculate_fish_social_state(
            fish=current_fish,
            all_fish=fish,
            neighbor_radius=neighbor_radius,
        )
        for current_fish in fish
    ]

    neighbor_counts = [
        state["neighbor_count"]
        for state in states
    ]

    nearest_neighbor_distances = [
        state["nearest_neighbor_distance"]
        for state in states
        if state[
            "nearest_neighbor_distance"
        ] is not None
    ]

    mean_neighbor_distances = [
        state["mean_neighbor_distance"]
        for state in states
        if state[
            "mean_neighbor_distance"
        ] is not None
    ]

    alignments = [
        state["alignment"]
        for state in states
        if state["alignment"] is not None
    ]

    cohesion_distances = [
        state["cohesion_distance"]
        for state in states
        if state["cohesion_distance"] is not None
    ]

    isolated_fish_count = sum(
        1
        for state in states
        if state["neighbor_count"] == 0
    )

    isolated_fish_fraction = (
        isolated_fish_count
        / len(states)
    )

    # --------------------------------------------------------------
    # Global descriptive metrics
    # --------------------------------------------------------------

    global_polarization = (
        _calculate_polarization(fish)
    )

    global_dispersion = (
        _calculate_dispersion(fish)
    )

    # --------------------------------------------------------------
    # Cluster / school metrics
    # --------------------------------------------------------------

    clusters = _find_clusters(
        fish=fish,
        neighbor_radius=neighbor_radius,
    )

    cluster_metrics = _calculate_cluster_metrics(
        clusters=clusters,
        all_fish=fish,
        neighbor_radius=neighbor_radius,
    )

    school_clusters = [
        cluster
        for cluster in cluster_metrics
        if cluster["cluster_size"] >= 2
    ]

    cluster_sizes = [
        cluster["cluster_size"]
        for cluster in cluster_metrics
    ]

    school_sizes = [
        cluster["cluster_size"]
        for cluster in school_clusters
    ]

    largest_cluster_size = max(
        cluster_sizes
    )

    largest_cluster_fraction = (
        largest_cluster_size
        / len(fish)
    )

    school_fish_count = sum(
        cluster["cluster_size"]
        for cluster in school_clusters
    )

    school_fish_fraction = (
        school_fish_count
        / len(fish)
    )

    school_polarizations = [
        cluster["polarization"]
        for cluster in school_clusters
        if cluster["polarization"] is not None
    ]

    school_dispersions = [
        cluster["dispersion"]
        for cluster in school_clusters
        if cluster["dispersion"] is not None
    ]

    return {
        "fish_count": len(fish),
        "isolated_fish_fraction": (
            isolated_fish_fraction
        ),
        "mean_neighbor_count": mean(
            neighbor_counts
        ),
        "mean_nearest_neighbor_distance": (
            _mean_or_none(
                nearest_neighbor_distances
            )
        ),
        "mean_neighbor_distance": (
            _mean_or_none(
                mean_neighbor_distances
            )
        ),
        "mean_alignment": (
            _mean_or_none(alignments)
        ),
        "mean_cohesion_distance": (
            _mean_or_none(
                cohesion_distances
            )
        ),

        # Global metrics describe the entire population.
        "global_polarization": (
            global_polarization
        ),
        "global_dispersion": (
            global_dispersion
        ),

        # Cluster metrics.
        "cluster_count": len(
            cluster_metrics
        ),
        "school_count": len(
            school_clusters
        ),
        "school_fish_fraction": (
            school_fish_fraction
        ),
        "largest_cluster_size": (
            largest_cluster_size
        ),
        "largest_cluster_fraction": (
            largest_cluster_fraction
        ),
        "mean_cluster_size": mean(
            cluster_sizes
        ),
        "mean_school_size": (
            _mean_or_none(
                school_sizes
            )
        ),
        "mean_school_polarization": (
            _mean_or_none(
                school_polarizations
            )
        ),
        "mean_school_dispersion": (
            _mean_or_none(
                school_dispersions
            )
        ),
        "clusters": cluster_metrics,
    }


def collect_school_social_snapshot(
    world: World,
) -> dict[str, Any]:
    """
    Collect one timestamped global and cluster-level snapshot.
    """
    return {
        "time": world.elapsed_time,
        **calculate_school_social_metrics(world),
    }


def collect_individual_social_snapshot(
    world: World,
) -> list[dict[str, Any]]:
    """
    Collect one timestamped social-state record
    for every living fish.
    """
    snapshots: list[dict[str, Any]] = []

    for fish in world.fish:
        social_state = (
            calculate_fish_social_state(
                fish=fish,
                all_fish=world.fish,
                neighbor_radius=(
                    world.config.neighbor_radius
                ),
            )
        )

        snapshots.append(
            {
                "time": world.elapsed_time,
                "fish_id": fish.fish_id,
                **social_state,
            }
        )

    return snapshots