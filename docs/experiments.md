# SchoolMind Experiment Metrics

## Iteration 6

Iteration 6 introduces measurements of fish schooling behavior.

These measurements are observational.

They do not change fish behavior.

The current Boids implementation remains the behavioral baseline.

---

## Local neighborhood

For fish `i`, its local neighborhood is defined as all other fish
within the configured `neighbor_radius`.

This matches the neighborhood definition currently used by Boids.

---

## Neighbor count

The number of neighboring fish within `neighbor_radius`.

A value of zero means the fish is locally isolated.

---

## Nearest-neighbor distance

The distance between a fish and its closest neighbor.

This describes local spacing.

We do not assume that smaller or larger values are automatically better.

---

## Mean-neighbor distance

The mean distance between a fish and all of its local neighbors.

This provides a broader measure of local spacing than the nearest-neighbor distance.

---

## Alignment

Alignment measures how similarly a fish is moving compared with
its local neighbors.

For each neighbor, directional similarity is calculated using
the cosine similarity of the normalized velocity vectors.

The result is transformed into the interval `[0, 1]`.

```text
0.0 → opposite directions
0.5 → perpendicular directions
1.0 → same direction

## Cohesion distance

The local neighborhood centroid is calculated.

The cohesion measurement is the distance between the fish and that centroid.

Smaller values indicate that the fish is closer to the center of its local group.

This is a measurement only. It does not define what the ideal distance should be.

---

## Polarization

Polarization measures how strongly the school is moving in a common direction.

It is calculated as the magnitude of the mean normalized velocity vector.

The range is `[0, 1]`.

```text
0.0 → highly mixed directions
1.0 → nearly identical movement direction
```

---

## Dispersion

The global school centroid is calculated.

Dispersion is the mean distance of living fish from that centroid.

Higher values indicate a more spatially dispersed school.

---

## Isolated-fish fraction

The fraction of living fish with zero local neighbors.

```text
isolated_fish_fraction =
    isolated_fish_count / living_fish_count
```

A lower value generally indicates that more fish are locally connected,
but this metric alone does not define whether the school is healthy.

---

## Time-series measurements

Social metrics are recorded throughout a trial instead of only at the end.

The sampling interval is controlled by:

```text
experiment.metrics_sample_interval
```

The default is `0.5` seconds.

This provides enough temporal resolution to study how social behavior
changes during predator encounters without storing a measurement
for every simulation frame.

---

## World boundaries

The simulation uses a bounded rectangular environment.

Fish and predators cannot wrap around the edges.

Entities begin turning away from nearby boundaries and are
hard-constrained to remain inside the world. If an entity reaches
a boundary, its corresponding velocity component is reflected.

Because the world is no longer toroidal, ordinary Euclidean
distance is appropriate for neighborhood and predator-distance
calculations.

---

## Future use

These measurements will eventually be used to investigate the
relationship between local social state and predation risk.

Iteration 6 does not yet define a "good school" mathematically.

That definition should emerge from analysis of the measured quantities
and their relationship to survival during Iteration 7.