# SchoolMind Experiment Metrics

## Purpose

Iteration 6 introduces quantitative measurements of fish social behavior.

These measurements are **observational only**.

They do not change fish behavior, predator behavior, or the simulation outcome.

The current Boids implementation remains the behavioral baseline.

The purpose of the measurements is to describe:

* the local social state of individual fish
* the structure of groups of fish
* the behavior of the entire fish population
* how these quantities change over time

These measurements will later support the Iteration 7 investigation of the relationship between social organization and predation risk.

---

## Simulation assumptions

Iteration 6 uses the following experimental assumptions.

### Fish speed

All fish use the same configured target speed.

Fish therefore do not have different inherent speed values that could independently affect their survival probability.

The current default is:

```text
fish_speed = 225.0
```

Fish can temporarily move below their target speed while accelerating or changing direction, but all fish have the same movement speed parameters.

### Predator spawning

Predators are spawned randomly throughout the environment.

There are no predator spawn-pattern behaviors such as ring, clustered, or opposite-side spawning.

Initial predator positions are still deterministic for a fixed random seed.

### World boundaries

The simulation uses a bounded rectangular environment.

Fish and predators cannot wrap around the edges.

Fish begin steering away from nearby boundaries using `fish_boundary_margin`, giving them room to turn before reaching a wall.

Predators use a boundary margin of `0`, allowing them to pursue fish all the way to the aquarium boundary.

Both fish and predators are hard-constrained to remain inside the environment.

If an entity reaches a boundary, its corresponding velocity component is reflected.

Because the world is not toroidal, ordinary Euclidean distance is used for neighborhood and predator-distance calculations.

---

## Local neighborhood

For fish `i`, its local neighborhood is defined as all other fish within the configured `neighbor_radius`.

This is the same neighborhood concept used by the current Boids implementation.

Conceptually:

```text
            neighbor
               ●

     ●                    ●
   neighbor              neighbor

               ●
              fish
```

Only fish within `neighbor_radius` are included in the local social-state calculations.

---

# Individual social-state metrics

These metrics describe the local social state of one fish.

They are calculated independently for every living fish.

## Neighbor count

The number of fish within `neighbor_radius`.

```text
neighbor_count_i = |N_i|
```

A value of zero means that the fish has no local neighbors and is therefore locally isolated.

This metric is descriptive only.

A larger neighbor count is not automatically considered better because extremely high local density can also represent overcrowding.

---

## Nearest-neighbor distance

The distance between a fish and its closest local neighbor.

```text
nearest_neighbor_distance_i =
    min(distance(i, j))
```

for all `j` in the fish's neighborhood.

This describes the closest local spacing around the fish.

A smaller value does not automatically represent a healthier state.

---

## Mean-neighbor distance

The average distance between a fish and all of its local neighbors.

```text
mean_neighbor_distance_i =
    average(distance(i, j))
```

for all `j` in the fish's neighborhood.

This provides a broader measure of local spacing than the nearest-neighbor distance.

As with nearest-neighbor distance, no ideal value is assumed during Iteration 6.

---

## Alignment

Alignment measures how similarly a fish is moving compared with its local neighbors.

For each neighbor, the normalized velocity vectors are compared using cosine similarity.

The cosine similarity is transformed from:

```text
[-1, 1]
```

into:

```text
[0, 1]
```

Interpretation:

```text
0.0 → opposite directions
0.5 → approximately perpendicular directions
1.0 → same direction
```

The fish's alignment is the mean of these neighbor-level alignment values.

A value near `1.0` indicates that the fish is moving in nearly the same direction as its local neighbors.

A value near `0.0` indicates strong directional disagreement.

---

## Cohesion distance

The centroid of the fish's local neighbors is calculated.

The cohesion measurement is the distance between the fish and that local centroid.

```text
cohesion_distance_i =
    distance(
        fish_i,
        local_neighbor_centroid
    )
```

Smaller values indicate that the fish is closer to the center of its local neighborhood.

This measurement does not define an ideal cohesion distance.

A value that is too large may indicate that the fish is leaving its local group, while an extremely small distance can also occur in highly crowded configurations.

---

# Population-level social metrics

These metrics describe the entire population of living fish.

They are useful for describing global behavior, but they should not be interpreted as direct measures of individual school formation.

---

## Mean neighbor count

The average `neighbor_count` across all living fish.

This provides a population-level indication of local connectivity.

---

## Mean nearest-neighbor distance

The average nearest-neighbor distance across all living fish.

This describes typical closest-neighbor spacing throughout the population.

---

## Mean neighbor distance

The average mean-neighbor distance across all living fish.

This provides a broader population-level spacing measurement.

---

## Mean alignment

The average individual alignment across all living fish.

This describes how similarly fish tend to move relative to their local neighbors.

Unlike global polarization, it is based on local relationships.

---

## Mean cohesion distance

The average individual cohesion distance across all living fish.

This provides a population-level description of how far fish typically are from their local neighborhood centroids.

---

## Isolated-fish fraction

The proportion of living fish with zero local neighbors.

```text
isolated_fish_fraction =
    isolated_fish_count / living_fish_count
```

A lower value generally indicates that more fish are locally connected.

However, this metric alone does not determine whether a healthy school exists.

---

# Global metrics

Global polarization and global dispersion describe the entire fish population.

They are **descriptive global metrics**.

They are not used to determine whether a school exists.

---

## Global polarization

Global polarization measures the directional coherence of the entire living fish population.

It is calculated as the magnitude of the mean normalized velocity vector across all fish.

The range is:

```text
0 → highly mixed or cancelling global directions
1 → the entire population moves in nearly the same direction
```

For example, consider two perfectly organized schools:

```text
School A
→ → → → →

School B
← ← ← ← ←
```

Each school may have very high internal directional coherence, while their directions cancel at the population level.

The result can therefore be:

```text
global_polarization ≈ 0
```

even though two well-organized schools exist.

For this reason, global polarization must not be interpreted as a schooling detector.

---

## Global dispersion

Global dispersion measures the spatial spread of the entire living fish population.

The global centroid is calculated from all living fish.

Then:

```text
global_dispersion =
    mean(
        distance(fish_i, global_centroid)
    )
```

Higher values indicate that the population as a whole is spatially spread out.

This is also a descriptive global metric.

For example:

```text
School A          School B

● ● ●             ● ● ●
 ● ●               ● ●
```

Each individual school can be compact while the two schools are far apart.

This produces:

```text
high global dispersion
low within-school dispersion
```

Therefore global dispersion does not directly measure school compactness.

---

# Cluster detection

Iteration 6 also identifies locally connected fish groups.

A cluster is defined using the existing `neighbor_radius`.

The fish are treated as nodes in a graph.

Two fish are directly connected when:

```text
distance(i, j) <= neighbor_radius
```

Clusters are the connected components of this graph.

This means indirect connections are allowed.

For example:

```text
A ─── B ─── C
```

can form one cluster even if `A` and `C` are more than `neighbor_radius` apart.

This approach is useful because schools are collective structures rather than collections of independent pairwise relationships.

---

## Cluster identity

Each cluster is assigned:

```text
cluster_id
```

using the smallest `fish_id` within that cluster.

This provides a deterministic identifier for the cluster within a particular snapshot.

A `cluster_id` should **not** be interpreted as a permanent identity across time.

For example, if one cluster splits into two clusters, their new cluster IDs may change.

Persistent tracking of school identity across time is not part of Iteration 6.

---

# Cluster-level metrics

Cluster-level metrics describe the organization of individual connected groups.

These are more appropriate than global metrics when asking whether multiple schools exist.

For every cluster, the following are recorded.

## Cluster size

The number of fish in the cluster.

```text
cluster_size
```

---

## Fish fraction

The proportion of living fish belonging to the cluster.

```text
fish_fraction =
    cluster_size / total_living_fish
```

---

## Mean alignment

The average individual alignment of fish within the cluster.

This describes internal directional coherence.

---

## Mean nearest-neighbor distance

The average nearest-neighbor distance within the cluster.

This describes typical closest-neighbor spacing inside the group.

---

## Mean neighbor distance

The average mean-neighbor distance within the cluster.

---

## Mean cohesion distance

The average cohesion distance of fish in the cluster.

This describes how far fish tend to be from their local neighborhood centers within the group.

---

## Cluster polarization

Polarization calculated using only the fish in that cluster.

```text
cluster_polarization =
    magnitude(
        mean(unit_velocity_i)
    )
```

Range:

```text
0 → mixed or cancelling directions
1 → highly coherent movement direction
```

Unlike global polarization, cluster polarization can identify coherent schools that move in different directions from one another.

---

## Cluster dispersion

Dispersion calculated relative to the centroid of that specific cluster.

```text
cluster_dispersion =
    mean(
        distance(fish_i, cluster_centroid)
    )
```

Higher values indicate that the cluster is more spatially spread out.

Lower values indicate that the cluster is more spatially compact.

---

# Cluster summary metrics

In addition to individual cluster records, population-level summaries of the detected clusters are recorded.

## Cluster count

The total number of connected components in the fish neighborhood graph.

This includes singleton clusters.

For example:

```text
A ●     B ●──● C     D ●
```

produces three clusters:

```text
[A]
[B, C]
[D]
```

---

## School count

The number of clusters containing at least two fish.

Singleton fish are not counted as schools.

Therefore:

```text
school_count <= cluster_count
```

---

## School fish fraction

The proportion of living fish belonging to a multi-fish cluster.

```text
school_fish_fraction =
    fish_in_multi_fish_clusters
    / total_living_fish
```

This is useful for distinguishing:

```text
many isolated fish
```

from:

```text
most fish participating in groups
```

---

## Largest cluster size

The number of fish in the largest detected cluster.

---

## Largest cluster fraction

The proportion of living fish belonging to the largest cluster.

```text
largest_cluster_fraction =
    largest_cluster_size
    / total_living_fish
```

---

## Mean cluster size

The average size across all clusters, including singleton clusters.

---

## Mean school size

The average size of multi-fish clusters only.

This excludes isolated fish.

---

## Mean school polarization

The mean polarization across multi-fish clusters.

This provides a summary of internal directional coherence across detected schools.

---

## Mean school dispersion

The mean dispersion across multi-fish clusters.

This provides a summary of the spatial compactness of detected schools.

---

# Interpreting multiple schools

The distinction between global and cluster-level metrics is important.

Consider:

```text
School A
→ → → →

School B
← ← ← ←
```

The measurements could show:

```text
global_polarization        ≈ 0
mean_school_polarization   ≈ 1
school_count               = 2
```

This means:

> The overall population has cancelling global directions, while each detected school is internally directionally coherent.

Similarly, two compact schools that are far apart can produce:

```text
high global_dispersion
low mean_school_dispersion
```

Therefore global metrics should be used to describe the overall population, while cluster metrics should be used to investigate individual schools.

---

# Time-series measurements

Social metrics are sampled throughout each experiment instead of being calculated only at the end.

The sampling frequency is controlled by:

```text
experiment.metrics_sample_interval
```

The current default is:

```text
0.5 seconds
```

A 30-second experiment therefore produces approximately 60 social measurement points.

These measurements allow us to study how collective behavior changes during the simulation.

For example:

```text
time
 ↓

0 s
    school structure

5 s
    school structure

10 s
    predator approaches

15 s
    school fragments

20 s
    fish regroup

25 s
    school structure stabilizes
```

This is important because a final snapshot cannot tell us when or how the school changed.

---

# Individual time series

Individual social measurements are recorded for every living fish at every sampling point.

Each record contains:

```text
time
fish_id
neighbor_count
nearest_neighbor_distance
mean_neighbor_distance
alignment
cohesion_distance
```

This allows a fish's social history to be reconstructed.

For example:

```text
Fish 37

t = 10.0
neighbors = 8
alignment = 0.91
cohesion_distance = 17

t = 10.5
neighbors = 7
alignment = 0.86
cohesion_distance = 21

t = 11.0
neighbors = 3
alignment = 0.58
cohesion_distance = 46
```

This information will be particularly important in Iteration 7 when social state is compared with predation outcomes.

---

# Capture events

Every capture is recorded separately from the periodic social measurements.

Each event contains:

```text
time
fish_id
predator_id
```

For example:

```text
{
    "time": 14.2167,
    "fish_id": 37,
    "predator_id": 1
}
```

This preserves the exact simulation time of the capture.

The capture time may fall between two social-metric sampling points.

The capture event should therefore not be treated as occurring at the nearest metric sample.

---

# Experiment output files

An experiment produces several complementary datasets.

```text
results.csv
```

Contains one row per trial.

It stores trial-level outcomes such as:

```text
fish_initial
fish_alive
fish_captured
survival_rate
capture_rate
time_elapsed
time_to_first_capture
time_to_extinction
predator_count
predator_target_switches
fish_speed
predator_coordination_mode
```

---

```text
social_metrics.csv
```

Contains one row per trial and timestamp.

It stores:

```text
global population metrics
cluster summary metrics
```

---

```text
cluster_social_metrics.csv
```

Contains one row per:

```text
trial × timestamp × cluster
```

It stores the structure and behavior of each detected cluster.

---

```text
individual_social_metrics.csv
```

Contains one row per:

```text
trial × timestamp × fish
```

It stores the local social state of each fish.

---

```text
capture_events.csv
```

Contains one row per captured fish.

It links:

```text
trial
seed
capture time
fish ID
predator ID
```

---

```text
results.json
```

Contains the complete nested experiment results, including trial results, social time series, individual social measurements, capture events, configuration, and summary information.

---

# Reproducibility

Every trial uses a deterministic random seed.

The trial seed is generated from the experiment's base seed:

```text
trial_seed =
    base_seed + trial_index - 1
```

The seed is stored with the trial results.

This ensures that an experiment can be reproduced using the same configuration and seed sequence.

---

# Iteration 6 research role

Iteration 6 does not yet define what constitutes a "healthy school."

In particular, it does not assume that:

```text
higher alignment = always better
lower cohesion distance = always better
lower dispersion = always better
more neighbors = always better
```

The purpose is to collect the underlying measurements first.

The next stage will investigate whether combinations of these social-state variables are associated with different predation outcomes.

Conceptually:

```text
individual social state
        │
        ├── separation / spacing
        ├── alignment
        ├── cohesion
        └── local connectivity
                 │
                 ↓
          predation outcome
                 │
                 ↓
              survival
```

This relationship will form the basis of the Iteration 7 social-state → predation-risk mechanism.

---

# Design principle

The most important distinction in Iteration 6 is:

```text
Boids parameters
        ↓
control current fish behavior

Social metrics
        ↓
measure the resulting behavior
```

The measurements do not influence the Boids fish.

This separation is intentional because future reinforcement-learning agents should eventually learn their movement policy without being controlled by the hand-coded separation, alignment, and cohesion rules.
