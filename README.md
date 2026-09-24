# SchoolMind — Sardine School Multi-Agent AI Project

## Project overview

**SchoolMind** is a progressive AI/ML project inspired by the collective behavior of sardine schools under predator attack.

The end goal is a visual, interactive research-style simulation in which individual fish behave as agents, learn predator-avoidance strategies, and exhibit collective behavior. An LLM-based research agent will eventually sit above the simulation and autonomously design experiments, run trials, analyze results, and explain findings.

The project is intentionally designed to be built **one iteration at a time in VS Code**. Each iteration should leave you with a working program that can be run, inspected, and demonstrated before moving to the next level.

---

# 1. End-state vision

The final application should look roughly like a small AI research laboratory.

```text
┌────────────────────────────────────────────────────────────────────┐
│                         SCHOOLMIND                                 │
│             Multi-Agent Predator / Prey Research Lab              │
├───────────────────────┬────────────────────────────────────────────┤
│                       │                                            │
│  SIMULATION           │            LIVE SIMULATION                 │
│                       │                                            │
│  Fish: 100            │        🐟 🐟 🐟 🐟 🐟                      │
│  Predator: 1          │      🐟 🐟 🐟 🐟 🐟 🐟                    │
│  Mode: RL             │    🐟 🐟 🐟 🐟 🐟 🐟 🐟                  │
│                       │               ↘                            │
│  [ Run ] [ Pause ]    │                 🗡️                       │
│  [ Reset ]            │                                            │
│                       │                                            │
├───────────────────────┴────────────────────────────────────────────┤
│ EXPERIMENT RESULTS                                                │
│                                                                    │
│ Survival Rate       87.0%                                         │
│ Time to First Catch 42.8 s                                        │
│ Regroup Time         2.4 s                                        │
│ School Dispersion   31.2 m                                        │
│                                                                    │
├────────────────────────────────────────────────────────────────────┤
│ AI RESEARCHER                                                      │
│                                                                    │
│ "Compare survival for school sizes 25, 50, 100, and 200."         │
│                                                                    │
│ → configured experiment                                           │
│ → ran 400 trials                                                  │
│ → analyzed results                                                │
│ → generated report                                                │
└────────────────────────────────────────────────────────────────────┘
```

The final system can contain four major layers:

1. **Simulation engine** — world, fish, predators, physics, time steps, and multi-predator coordination.
2. **Behavior / ML layer** — rule-based schooling, then learned policies.
3. **Experiment layer** — repeatable trials, metrics, datasets, evaluation.
4. **AI researcher layer** — LLM agent that operates the experiment framework through tools.

---

# 2. Main learning objectives

By completing the project, you should gain practical experience in:

- Python project structure and software design
- Numerical simulation and vector-based movement
- Emergent behavior
- Boids / local-interaction models
- Feature engineering for agents
- Reinforcement learning fundamentals
- Neural-network policies
- Reward design
- Experience collection and training loops
- Multi-agent reinforcement learning concepts
- Environment design and evaluation
- Experiment reproducibility
- Visualization and data analysis
- LLM tool use / AI agents
- Agent planning and iterative experimentation
- Building a portfolio-grade AI project

The project should emphasize **understanding the mechanisms**, not simply calling a prebuilt AI API.

---

# 3. Recommended development stack

Use a Python-first stack so the simulation, ML, experimentation, and AI-agent components can eventually live in one repository.

### Core

- Python
- VS Code
- Git + GitHub
- Virtual environment (`.venv`)

### Simulation / visualization

Start with a lightweight 2D simulation framework such as:

- Pygame for the initial visual simulation

A web-based visualization can be added later if desired, but it should **not** be the first version. The priority is understanding the simulation and ML architecture.

### ML / RL

Use:

- NumPy
- PyTorch
- Gymnasium-style environment interfaces where useful
- A multi-agent environment framework such as PettingZoo when the project reaches multi-agent RL

Do not lock the project to exact dependency versions in this planning document; pin versions in `requirements.txt` or a lockfile once you create the environment.

### Data / analysis

- pandas
- matplotlib

### AI agent layer

Use the Hugging Face agent concepts from the course you are following. Keep the research-agent integration modular so the simulation itself remains independent from any one LLM provider.

---

# 4. Repository structure

Start small, but use a structure that can grow.

```text
SchoolMind/
│
├── README.md
├── pyproject.toml              # or requirements.txt initially
├── .gitignore
├── .env.example
│
├── src/
│   └── schoolmind/
│       ├── __init__.py
│       │
│       ├── simulation/
│       │   ├── world.py
│       │   ├── fish.py
│       │   ├── predator.py
│       │   ├── physics.py
│       │   └── config.py
│       │
│       ├── behavior/
│       │   ├── boids.py
│       │   ├── rules.py
│       │   └── policies.py
│       │
│       ├── rl/
│       │   ├── environment.py
│       │   ├── observations.py
│       │   ├── rewards.py
│       │   ├── networks.py
│       │   └── training.py
│       │
│       ├── multiagent/
│       │   ├── environment.py
│       │   ├── agents.py
│       │   └── training.py
│       │
│       ├── experiments/
│       │   ├── runner.py
│       │   ├── metrics.py
│       │   ├── scenarios.py
│       │   └── analysis.py
│       │
│       ├── researcher/
│       │   ├── agent.py
│       │   ├── tools.py
│       │   └── prompts.py
│       │
│       └── visualization/
│           ├── renderer.py
│           ├── overlays.py
│           └── plots.py
│
├── tests/
│   ├── test_physics.py
│   ├── test_boids.py
│   ├── test_rewards.py
│   └── test_experiments.py
│
├── configs/
│   ├── baseline.yaml
│   ├── rl.yaml
│   └── experiments.yaml
│
├── notebooks/
│   └── analysis.ipynb
│
├── runs/
│   └── .gitkeep
│
└── docs/
    ├── architecture.md
    ├── experiments.md
    └── research_notes.md
```

The exact structure can evolve. Do not create every file on day one.

## Multi-predator design principle

Multiple predators are a supported scenario throughout the project, even if the earliest visual demo starts with one. Build the core simulation around a **collection of predators** rather than hard-coding a single predator.

Conceptually:

```python
predators = [Predator(...), Predator(...), Predator(...)]
```

Each predator should have its own state (position, velocity, speed, target, behavior), while the world owns the collection and updates them each simulation step. Fish observations should be able to represent **the nearest threat, the top-K threats, or aggregated threat information** depending on the experiment.

This gives us a clean progression:

```text
1 predator
    ↓
2 predators
    ↓
5+ predators
    ↓
coordinated / independent predators
    ↓
learned predator strategies (optional research extension)
```

Do not assume that multiple predators behave like one stronger predator. Different spatial configurations, approach angles, speeds, and coordination strategies can create qualitatively different behavior.

---

# 5. Development philosophy

For every iteration:

1. Build the smallest useful version.
2. Make it runnable from VS Code.
3. Test it.
4. Observe the behavior visually.
5. Add metrics.
6. Commit the working state to Git.
7. Write down what you learned.
8. Only then move to the next iteration.

Avoid jumping straight into reinforcement learning. The earlier simulation work is not throwaway work; it becomes the environment that the learning agents will eventually inhabit.

---

# 6. Iteration roadmap

## Iteration 0 — Development environment

### Goal

Create a clean Python repository that can be developed and run entirely from VS Code.

### Tasks

- Install Python and VS Code.
- Install the Python extension for VS Code.
- Install Git.
- Create the Git repository.
- Create `.venv`.
- Configure the VS Code interpreter to use `.venv`.
- Create the initial package structure.
- Add `.gitignore`.
- Create a minimal `README.md`.
- Add a simple entry point such as:

```bash
python -m schoolmind
```

or a small `main.py` during the earliest stage.

### Deliverable

A repository that opens cleanly in VS Code and runs a Python program successfully.

### Definition of done

- `git status` is clean after committing the initial project.
- Python executes from the VS Code terminal.
- A simple SchoolMind program runs without errors.

---

# Iteration 1 — 2D fish simulation

## Goal

Create a visual environment containing fish that move around a 2D world.

### Build

Create:

- A fixed-size simulation window.
- A `Fish` class.
- Position `(x, y)`.
- Velocity `(vx, vy)`.
- Speed limit.
- Maximum turn rate.
- Frame/time-step update.
- Simple fish rendering.

At this stage the fish can move randomly or follow a basic direction.

### Concept to learn

Separate **simulation state** from **rendering**.

The fish should have data representing what is happening, while the renderer only displays that state.

### Deliverable

A window containing multiple moving fish.

### Definition of done

- 50+ fish can run smoothly.
- Fish remain within the world or wrap around the edges.
- Movement is represented with vectors.
- Simulation logic is not embedded entirely inside rendering code.

### Git checkpoint

`iteration-1-basic-simulation`

---

# Iteration 2 — Individual fish behavior

## Goal

Give each fish basic physical constraints and predictable motion.

### Add

- Maximum speed.
- Maximum acceleration.
- Maximum turning rate.
- Optional random perturbation.
- Velocity normalization.
- Boundary handling.

### Learn

Understand:

- Vectors
- Acceleration
- Steering forces
- Time-step integration

### Deliverable

Fish that move continuously and naturally rather than teleporting or changing direction instantly.

### Definition of done

You can explain exactly how the position and velocity of a fish change every simulation step.

---

# Iteration 3 — Schooling with Boids-style rules

## Goal

Produce school-like collective behavior without machine learning.

### Implement three core rules

#### 1. Separation

Move away from nearby fish that are too close.

#### 2. Alignment

Move toward the average heading / velocity of nearby fish.

#### 3. Cohesion

Move toward the local group's center.

You may later add:

- boundary avoidance
- velocity matching
- noise
- attraction/repulsion zones

### Important architectural idea

The fish should not directly know the global state of the world.

For example, each fish should ideally calculate behavior from a local neighborhood:

```text
my fish
   ↓
nearby fish
   ↓
local information
   ↓
steering decision
```

### Deliverable

A visually convincing school emerges from local rules.

### Experiment

Try changing:

- school size
- neighborhood radius
- separation strength
- alignment strength
- cohesion strength

Record what happens.

### Definition of done

You can produce noticeably different collective patterns by changing a small set of parameters.

### Git checkpoint

`iteration-3-emergent-schooling`

---

# Iteration 4 — Introduce predators

## Goal

Add the first swordfish/predator **while designing the simulation to support any number of predators**. One predator is simply the first scenario.

### Predator model

Create a reusable `Predator` entity with at least:

- position
- velocity
- maximum speed
- maximum acceleration / turning rate
- detection range
- capture radius
- current target (optional)
- predator ID

Create a world-level predator collection or `PredatorManager` responsible for spawning, updating, and removing predators.

### First behavior

Start with a simple hand-coded strategy:

- identify a target fish
- move toward the target
- optionally pursue the target's predicted future position
- capture fish within the capture radius

For one predator, the target can initially be the nearest fish.

### Fish response

Add **predator avoidance**. Each fish should evaluate nearby predators and steer away from immediate threats.

A simple first rule is:

```text
avoidance_force = sum(repulse(predator_i) for predator_i in nearby_predators)
```

This is intentionally a simple baseline. Later iterations can learn how to combine multiple threats.

### Multi-predator scenarios

Add configuration support for:

```yaml
predator_count: 1
```

Then verify at least these scenarios:

```text
1 predator → baseline
2 predators → simultaneous threats
3+ predators → threat saturation / complex movement
```

Predators should not be assumed to share a target unless the scenario explicitly specifies coordination.

### Visualization

Add visual cues for:

- predator detection radius
- each predator ID or color/shape distinction
- each predator's current target
- capture events
- school boundaries / centroid
- optional threat vectors from fish to nearby predators

### Metrics

Start recording:

- number of fish alive
- number captured
- time until first capture
- time to extinction / final capture (when relevant)
- average distance to nearest predator
- average distance to all relevant predators
- school diameter
- school centroid
- average speed
- predator-target switches
- number of active predators

### Deliverable

A complete baseline predator-vs-school simulation that works with **one or many predators without changing core fish or world logic**.

### Definition of done

You can switch `predator_count` from 1 to 2 or 5 in configuration, run the simulation, and obtain sensible behavior and metrics without modifying source code.

---

# Iteration 5 — Build a real experiment framework

## Goal

Turn the simulation into an experimental platform.

### Build

Create a configuration object/file containing parameters such as:

```yaml
school_size: 100
predator_count: 1
predator_speed: 1.5
predator_spawn_pattern: ring
predator_targeting: nearest_fish
simulation_duration: 60
random_seed: 42
separation_weight: 1.0
alignment_weight: 1.0
cohesion_weight: 1.0
avoidance_weight: 2.0
```

### Add

- deterministic random seeds
- batch runs
- result files
- experiment IDs
- summary statistics
- scenario definitions for 1, 2, 3, 5, or more predators
- predator spawn patterns (clustered, opposite sides, ring, random)
- independent vs coordinated predator behavior

### Example command

```bash
python -m schoolmind.experiments.runner --config configs/baseline.yaml
```

### Deliverable

One command should be capable of running many simulations and producing structured results.

### Definition of done

You can run 100 simulations with different random seeds and summarize the results automatically.

### Git checkpoint

`iteration-5-experiment-framework`

---

# Iteration 6 — Define and measure the schooling state

## Goal

Turn the biological idea of a sardine school into measurable quantities that can later be used to determine whether an individual fish is meaningfully integrated into a school.

The purpose of this iteration is **not** to train anything.

The purpose is to answer:

> **What does it mathematically mean for one fish to be part of a healthy school?**

The three core components remain:

1. **Separation** — nearby fish should not become excessively crowded.
2. **Alignment** — neighboring fish should have similar movement directions.
3. **Cohesion** — a fish should remain connected to its local group rather than becoming isolated.

These quantities should be measured primarily from a fish's **local neighborhood**, because the eventual RL agents should not depend on global knowledge of the entire school.

---

## Individual social state

For each fish, calculate a local social state from its nearby neighbors.

Conceptually:

```text
                nearby fish
                     │
          ┌──────────┼──────────┐
          ↓          ↓          ↓
      separation  alignment   cohesion
          │          │          │
          └──────────┼──────────┘
                     ↓
            individual social state
```

The exact mathematical definitions should be documented in:

```text
docs/experiments.md
```

before implementation.

### Separation

Measure how appropriately spaced the fish is relative to its local neighbors.

The goal is not:

```text
more distance = better
```

or:

```text
less distance = better
```

Instead, we want a **healthy spacing range**.

A fish that is extremely close to another fish should have poor separation.

A fish that is extremely far from all neighbors may also indicate that it is leaving the school.

### Alignment

Measure how closely the fish's velocity direction matches the average direction of nearby fish.

A simple normalized directional similarity can be used initially.

### Cohesion

Measure how connected the fish is to its local group.

This can be represented using distance to a local neighborhood centroid or another local-density measure.

Again, there should be a healthy range rather than simply rewarding the smallest possible distance.

---

## School-level metrics

Aggregate individual measurements into trial-level metrics such as:

```text
mean separation quality
mean alignment
mean cohesion
school dispersion
school polarization
fraction of fish considered socially integrated
```

The most important new metric is:

### Social integration rate

The percentage of living fish whose local separation, alignment, and cohesion all fall inside the defined healthy ranges.

For example:

```text
social integration rate = 82%
```

This gives us a direct quantitative representation of how many fish are actually participating in a coherent school.

---

## Time-series measurements

Metrics should be sampled throughout a trial rather than only calculated at the end.

For example:

```text
time
  ↓
0s ──── 5s ──── 10s ──── 15s ──── 20s
       │         │          │
      school state recorded
```

This allows us to later measure:

* how quickly a school forms
* how quickly a predator disrupts it
* how long fish remain socially integrated
* how quickly the school recovers
* whether social integration changes before capture

---

## Deliverable

A measurement layer capable of producing:

```text
individual social state
        ↓
time-series measurements
        ↓
trial metrics
        ↓
batch-level summaries
```

with reproducible results.

### Definition of done

For a given simulation state, we can calculate and explain:

```text
separation
alignment
cohesion
social integration
dispersion
polarization
```

for individual fish and for the school as a whole.

### Git checkpoint

`iteration-6-schooling-metrics`

---

# Iteration 7 — Establish the social-state → predation-risk mechanism

## Goal

Introduce the central mechanism of the entire SchoolMind research project:

> **A fish that is poorly integrated into the school should be more vulnerable to predation than a fish that is properly integrated.**

This is the critical bridge between the simulation and the future RL problem.

At the end of this iteration, the environment should contain a measurable relationship between:

```text
local social state
        ↓
predation vulnerability
        ↓
survival
```

---

## Important principle

We should **not** tell the fish:

```text
"Stay close to the school."
```

Instead, the environment should make schooling advantageous through survival.

Conceptually:

```text
healthy social state
        ↓
lower capture risk
        ↓
higher survival

poor social state
        ↓
higher capture risk
        ↓
lower survival
```

The fish will eventually discover this relationship through reinforcement learning.

---

## Vulnerability model

The predator's baseline ability to capture a fish should be combined with a social-vulnerability modifier.

Conceptually:

```text
capture probability
    =
baseline predator risk
×
social vulnerability
```

The social vulnerability term should depend on the fish's local:

```text
separation
alignment
cohesion
```

A fish outside the healthy schooling region should become more vulnerable.

A fish inside the healthy schooling region should become less vulnerable.

The exact functional form should be kept simple initially and documented before implementation.

For example, the first version could use a bounded multiplier:

```text
social vulnerability ∈ [low risk, high risk]
```

rather than immediately creating a complicated biological model.

---

## Do not hard-code a perfect school

The environment should not simply say:

```text
if distance_to_centroid < X:
    fish is safe
```

That would make "schooling" equivalent to one arbitrary geometric rule.

Instead, the mechanism should consider the combination of:

```text
separation
alignment
cohesion
```

so that the agent eventually has an incentive to discover a **healthy local configuration**.

---

## Avoid an unrealistic discontinuity

Avoid:

```text
healthy school → completely safe
not healthy → guaranteed death
```

The relationship should be probabilistic.

Even a well-integrated fish can be captured.

Even an isolated fish can survive.

The difference should be in **probability over many trials**, not deterministic protection.

---

## Validation before RL

Before introducing reinforcement learning, use the existing rule-based fish to verify that the environment behaves sensibly.

Controlled experiments should compare fish in different social states.

For example:

```text
well-integrated fish
moderately isolated fish
poorly aligned fish
overcrowded fish
```

Then evaluate their capture outcomes across many randomized trials.

The purpose is not to prove a biological law.

The purpose is to verify that the computational environment actually contains the intended learning signal.

---

## Important research constraint

The relationship should be strong enough for learning to discover but not so strong that schooling becomes an explicit scripted solution.

We want:

```text
predation pressure
       ↓
survival differences
       ↓
learning signal
       ↓
emergent schooling
```

not:

```text
schooling rule
       ↓
fish follows it
```

---

## Deliverable

A validated baseline predation-risk model in which local social state measurably affects capture probability.

### Definition of done

Across repeated trials, the experiment framework can demonstrate that social integration changes survival outcomes while keeping the predator, world, and trial conditions controlled.

### Git checkpoint

`iteration-7-social-predation-risk`

---

# Iteration 8 — Build the reinforcement-learning environment

## Goal

Convert the validated simulation into an RL environment.

This is the transition from:

```text
hand-coded simulation
```

to:

```text
learning environment
```

---

## Start with one learning fish

Do **not** make all fish learn immediately.

Start with:

```text
1 learning fish
+
rule-based school
+
1 predator
```

The rest of the fish continue using the established Boids behavior.

This isolates the learning problem.

The learning fish should have to determine how to move while experiencing the consequences of its social state and predator exposure.

---

## Observation design

The observation should contain only information reasonably available to the individual fish.

A first version could include:

```text
own velocity

nearest-neighbor distance
local average neighbor direction
local centroid direction

local separation measure
local alignment measure
local cohesion measure

nearest predator distance
nearest predator relative direction

optional local threat information
```

The important point is that we should expose **local state**, not a global instruction.

For example:

```text
DO NOT:
"the school is currently 37 meters wide"

PREFER:
"my nearest neighbors are this far away"
```

The observation space should remain small.

---

## Action space

Start with a small discrete action space:

```text
turn left
maintain heading
turn right
accelerate
decelerate
```

Continuous steering can come later.

---

## Environment interface

Implement standard:

```text
reset()
step(action)
```

with:

```text
observation
      ↓
action
      ↓
simulation step
      ↓
new observation
      ↓
reward
      ↓
done
```

---

## Deliverable

A functioning environment that can run a random policy from start to finish.

### Definition of done

A learning fish can interact with the simulation without any RL algorithm being required yet.

### Git checkpoint

`iteration-8-rl-environment`

---

# Iteration 9 — Design a survival-driven reward

## Goal

Design the reward so that the environment encourages survival without directly instructing the agent to perform schooling.

This is one of the most important iterations in the project.

---

## Primary principle

The eventual goal is:

> **Schooling should emerge because schooling improves survival, not because the reward explicitly tells fish to school.**

Therefore, the first reward should be deliberately simple.

Conceptually:

```text
+ small reward for surviving
- large penalty for capture
```

The major schooling signal should come indirectly through the environment:

```text
healthy school state
      ↓
lower capture probability
      ↓
higher expected future reward
```

---

## Avoid this initially

Do not start with:

```text
+ alignment
+ cohesion
+ separation
+ predator distance
+ school centroid proximity
+ etc.
```

because that risks turning the reward function itself into a hand-coded Boids objective.

For example:

```text
reward += cohesion
```

would make the experiment much less interesting because we explicitly told the agent that cohesion is good.

---

## Reward shaping as a later experiment

Small shaping terms can be introduced later if training proves difficult.

However, every additional reward component should answer:

> Is this helping the fish discover the intended survival strategy, or am I manually programming the behavior?

This distinction should be maintained throughout the project.

---

## Reward validation

Before large training runs, evaluate several reward configurations using short experiments.

Track:

```text
episode reward
survival time
capture rate
social integration
schooling metrics
```

The objective is to detect unintended incentives.

For example:

```text
agent learns to flee indefinitely
```

would be a warning that the reward/environment combination is not producing the desired problem.

---

## Deliverable

A documented first reward formulation and small validation experiments.

### Definition of done

The reward is understandable mathematically, reproducible, and does not directly encode "form a school" as the primary objective.

### Git checkpoint

`iteration-9-survival-reward`

---

# Iteration 10 — Train the first learning fish

## Goal

Train a single fish to survive inside the rule-based school.

The first major hypothesis test is:

> **Can an individual fish learn behavior that improves its survival while remaining socially integrated?**

---

## Training setup

Start with:

```text
1 learning fish
+
rule-based school
+
1 predator
```

Do not immediately train on every predator configuration.

First establish that learning works in the simplest environment.

---

## Build

Implement:

* policy network
* experience collection
* training loop
* checkpointing
* evaluation mode
* deterministic evaluation seeds

---

## Monitor

Track at minimum:

```text
episode reward
survival time
capture rate
social integration
separation
alignment
cohesion
```

The most important question is not merely:

```text
Did reward increase?
```

but:

```text
Did survival improve while the fish remained connected to the school?
```

---

## Visualization

Show the learning fish with a visible marker.

Provide comparison modes:

```text
Rule-based fish
vs
Learning fish
```

---

## Deliverable

A trained model that can be loaded and evaluated independently of training.

### Definition of done

The training pipeline is reproducible and the trained fish can be evaluated across multiple trials.

### Git checkpoint

`iteration-10-first-learning-fish`

---

# Iteration 11 — Controlled evaluation of the learned strategy

## Goal

Determine what the first learning agent actually learned.

Do not assume that increased survival means successful schooling.

---

## Compare

Run controlled experiments between:

```text
random policy
rule-based fish
trained learning fish
```

under the same environmental conditions.

---

## Measure

For each policy, record:

```text
survival rate
time to capture
social integration rate
separation
alignment
cohesion
dispersion
predator distance
```

---

## Critical analysis

Look for relationships such as:

```text
social integration ↑
        ↓
capture probability ↓
        ↓
survival ↑
```

The purpose of this stage is to determine whether the environment is producing the behavior we intended to study.

A model that survives by simply fleeing far away should not be considered successful merely because it has a high survival score.

---

## Ablation experiments

Remove or alter individual information components:

```text
without social observations
without alignment information
without cohesion information
without separation information
```

This helps determine whether the learned strategy actually depends on local social information.

---

## Deliverable

A quantitative evaluation report describing the behavior of the first learning agent.

### Definition of done

We can distinguish:

```text
survival improvement
```

from:

```text
successful social predator avoidance
```

using measured results.

---

# Iteration 12 — Multi-agent reinforcement learning

## Goal

Move from one learning fish to an entire school of learning fish.

This is the point where decentralized learning becomes the central experiment.

---

## Setup

Replace:

```text
1 learning fish
+
rule-based fish
```

with:

```text
all fish = learning agents
```

Each agent should have:

```text
local observation
policy
action
reward
state transition
```

---

## Shared policy

Start with parameter sharing so all fish can use the same policy.

Conceptually:

```text
Fish 1 ─┐
Fish 2 ─┤
Fish 3 ─┼──→ shared policy
Fish 4 ─┤
Fish N ─┘
```

Each fish still receives its own local observation and takes its own action.

This keeps the first multi-agent problem manageable.

---

## Implicit communication

Do not give the agents explicit messages such as:

```text
"move toward the center"
"everyone turn left"
"predator approaching from the east"
```

Coordination should emerge through:

```text
local observations
+
shared environment
+
individual actions
+
shared consequences
```

---

## Predator scenarios

Once the one-predator case is working, extend evaluation to:

```text
1 predator
2 predators
3+ predators
```

using the scenarios already supported by the simulation.

---

## Deliverable

A school consisting entirely of learning agents.

### Definition of done

The simulation can run a fully learned school through repeated predator-attacked episodes.

### Git checkpoint

`iteration-12-multi-agent-learning`

---

# Iteration 13 — Test whether schooling actually emerges

## Goal

This is the central scientific evaluation of SchoolMind.

The question becomes:

> **Can decentralized fish agents develop schooling behavior because schooling improves survival?**

---

## Primary hypothesis

We expect that agents may discover that being:

```text
appropriately separated
+
aligned with neighbors
+
cohesively connected
```

reduces their probability of capture.

However, this should be treated as an empirical hypothesis.

The results may show:

```text
strong schooling
partial schooling
different collective behavior
failure to school
```

All of these outcomes are informative.

---

## Compare

Evaluate:

```text
A. rule-based Boids school

B. independently trained learning fish

C. jointly trained multi-agent school
```

Where useful, also evaluate:

```text
D. agents with restricted social observations
```

---

## Key measurements

Measure both individual and collective behavior:

```text
capture probability
survival time
separation
alignment
cohesion
social integration rate
dispersion
polarization
regrouping time
```

---

## Most important analysis

Analyze the relationship between an individual fish's social state and its subsequent capture outcome.

Conceptually:

```text
social state at time t
          ↓
capture probability during t → t + Δt
```

This is much closer to the original biological idea than simply looking at whether the school "looks good."

---

## Deliverable

A research-style report answering:

> Did schooling emerge from survival-driven decentralized learning?

The report should include both quantitative measurements and visual examples.

---

# Iteration 14 — Ablation, robustness, and generalization

## Goal

Determine whether the learned behavior is genuinely dependent on the intended mechanism or is exploiting an accidental feature of the simulation.

---

## Ablation studies

Test variants such as:

```text
A. normal social-risk model

B. no social-risk advantage

C. reduced social-risk advantage

D. no alignment information

E. no cohesion information

F. no separation information
```

The purpose is to determine which parts of the environment and observation space matter.

---

## Generalization

Train under one set of conditions and evaluate under unseen conditions.

For example:

```text
TRAIN
school size: 100
predator count: 1
predator speed: 1.5
```

Then evaluate under:

```text
school size: 50
school size: 200

predator count: 2
predator count: 3

different predator speeds

different predator spawn patterns
```

---

## Why this matters

A policy that only survives under exactly the conditions used during training may have learned a narrow strategy rather than a more general behavior.

---

## Deliverable

A generalization and ablation matrix showing how behavior changes under controlled modifications.

---

# Iteration 15 — Build the experiment and evaluation interface

## Goal

Turn the experiment framework into a reusable research API capable of comparing policies, environmental mechanisms, and training configurations.

---

## Core operations

The experiment system should eventually expose functions such as:

```text
create_scenario()
run_trial()
run_batch()
calculate_metrics()
load_model()
evaluate_model()
compare_models()
compare_experiments()
generate_report()
```

---

## Example

A future experiment could request:

```text
Compare:

1. rule-based fish
2. trained single-agent policy
3. trained multi-agent policy

across:

- school sizes 50, 100, 200
- 1, 2, and 3 predators
- multiple predator spawn patterns

Report:

- survival
- capture probability
- social integration
- cohesion
- alignment
- dispersion
```

The existing reproducibility system from Iteration 5 should remain the foundation for this work.

---

## Deliverable

A reusable evaluation layer that allows experiments to be defined without modifying simulation source code.

---

# Iteration 16 — Hugging Face AI Researcher

## Goal

Connect SchoolMind to the Hugging Face AI Agents concepts being learned in parallel.

The LLM should **not control individual fish**.

Instead, it becomes a researcher that operates the experiment system.

---

## Architecture

```text
User research question
        ↓
AI researcher
        ↓
experiment tools
        ↓
SchoolMind simulation
        ↓
structured results
        ↓
analysis
        ↓
AI researcher
        ↓
research-style explanation
```

---

## Example request

```text
Investigate whether increasing school size
changes the relationship between social integration
and survival under predatory attack.
```

The researcher could:

```text
create experiment
        ↓
run trials
        ↓
retrieve metrics
        ↓
compare conditions
        ↓
generate plots
        ↓
summarize findings
```

---

## Important constraint

The LLM must not invent numerical results.

The deterministic SchoolMind code should:

```text
run simulation
calculate metrics
produce results
```

while the LLM:

```text
interprets
explains
and communicates
```

those results.

---

## Deliverable

A working research agent capable of operating SchoolMind through defined tools.

### Git checkpoint

`iteration-16-ai-researcher`

---

# Iteration 17 — Research memory and visual dashboard

## Goal

Give the project a polished research interface and persistent experiment history.

---

## Experiment history

Each experiment should retain:

```text
experiment ID
research question
configuration
random seeds
environment configuration
model/checkpoint
reward configuration
metrics
plots
timestamp
analysis
```

The researcher should be able to refer to previous experiments by ID.

---

## Dashboard

The eventual interface should contain:

### Simulation

```text
live simulation
play / pause / reset
scenario selection
predator configuration
model selection
```

### Metrics

```text
survival
capture probability
social integration
separation
alignment
cohesion
dispersion
regrouping
```

### Experiments

```text
create experiment
run batch
compare experiments
inspect trajectories
```

### AI Researcher

```text
research question
tool execution
experiment history
analysis
generated report
```

---

## Deliverable

A single interface capable of demonstrating the complete SchoolMind workflow.

---

# Iteration 18 — Final research and portfolio presentation

## Goal

Turn SchoolMind into a complete, reproducible research-style AI project.

The final project should demonstrate the progression:

```text
hand-coded schooling
        ↓
predatory attack
        ↓
measurable social state
        ↓
social state affects predation risk
        ↓
RL environment
        ↓
individual learning
        ↓
multi-agent learning
        ↓
emergent collective behavior
        ↓
controlled experiments
        ↓
AI research agent
```

---

## Final README should explain

1. Biological motivation
2. Research hypothesis
3. Simulation architecture
4. Boids baseline
5. Predator model
6. Social-state definitions
7. Predation-risk model
8. RL environment
9. Reward design
10. Multi-agent architecture
11. Experimental methodology
12. Results
13. Ablation studies
14. Generalization experiments
15. AI researcher architecture
16. How to reproduce the experiments
17. How to run the project locally
18. Future research directions

---

# Suggested milestone timeline

The roadmap now follows the research logic of the project:

```text
FOUNDATION
│
├── 0. Development environment
├── 1. Basic simulation
├── 2. Fish physics
│
▼
RULE-BASED BASELINE
│
├── 3. Boids schooling
├── 4. Predator simulation
├── 5. Experiment framework
│
▼
RESEARCH MECHANISM
│
├── 6. Measure schooling state
├── 7. Establish social-state → predation-risk mechanism
│
▼
SINGLE-AGENT LEARNING
│
├── 8. RL environment
├── 9. Survival-driven reward
├── 10. First learning fish
├── 11. Controlled evaluation
│
▼
MULTI-AGENT LEARNING
│
├── 12. Multi-agent RL
├── 13. Emergent schooling experiments
├── 14. Ablation / robustness / generalization
│
▼
RESEARCH PLATFORM
│
├── 15. Experiment and evaluation interface
├── 16. AI researcher
├── 17. Research memory + dashboard
│
▼
PORTFOLIO
│
└── 18. Final research presentation
```

---

# Core research question

The entire project should ultimately revolve around one central question:

> **Can decentralized reinforcement-learning agents develop schooling behavior because being socially integrated reduces their probability of being captured by predators?**

This question should guide the design of the environment, observations, rewards, experiments, and evaluation.

---

# Secondary research questions

Once the central mechanism works, the following become natural extensions.

### School size

Does school size change the survival advantage of social integration?

### Predator pressure

How does the relationship between schooling and survival change as predator speed or predator count increases?

### Local information

How much information about nearby fish is necessary for useful schooling to emerge?

### Separation, alignment, and cohesion

Which aspects of local social state contribute most strongly to reduced predation risk and successful collective behavior?

### Predator geometry

Does the spatial arrangement of predators change the effectiveness of schooling?

### Communication

Can useful collective behavior emerge without explicit inter-agent communication?

### Generalization

Does a learned schooling strategy transfer to unseen school sizes, predator configurations, and attack scenarios?

---

# What not to do

Do not jump directly into complex RL algorithms.

Do not make every fish learn before the single-agent problem is understood.

Do not use a giant observation vector "just in case."

Do not define the reward primarily as:

```text
reward = alignment + cohesion + separation
```

because that directly programs the behavior we want to observe emerging.

Do not make socially integrated fish invulnerable.

Do not make isolated fish automatically die.

Do not judge learning from one simulation.

Do not treat visual schooling as proof of successful learning.

Do not change many experimental variables simultaneously when testing a hypothesis.

Do not add the LLM researcher until the simulation and experiment framework can produce trustworthy results without it.

---

# Reproducibility requirements

Every experiment should record enough information to reproduce the result.

At minimum:

```text
experiment_id
random_seed
school_size
predator_count
predator_speed
predator_spawn_pattern
predator_coordination_mode
simulation_duration
behavior_model
RL_model/checkpoint
reward configuration
environment configuration
social-risk configuration
metrics
```

A result should always be traceable to the exact conditions that produced it.

---

# Testing strategy

Tests should be added continuously.

## Simulation tests

Examples:

```text
fish movement is correct
velocity limits are respected
separation produces the expected steering direction
predator capture occurs correctly
```

## Social-state tests

Examples:

```text
separation metric is correct
alignment metric is correct
cohesion metric is correct
social integration classification is deterministic
```

## Predation-risk tests

Examples:

```text
social risk stays within configured bounds
healthy social state reduces expected capture risk
poor social state increases expected capture risk
risk remains probabilistic
```

## Experiment tests

Examples:

```text
random seeds are reproducible
batch runner creates the expected number of trials
metrics are deterministic for a fixed trial
results preserve experiment configuration
```

## RL tests

Examples:

```text
environment reset works
environment step returns valid data
observations have the expected shape
actions are accepted correctly
checkpoints save and load
evaluation can run without exploration
```

---

# Suggested Git workflow

Maintain clear checkpoints for major research stages.

```text
iteration-1-basic-simulation
iteration-2-fish-physics
iteration-3-emergent-schooling
iteration-4-predator
iteration-5-experiment-framework
iteration-6-schooling-metrics
iteration-7-social-predation-risk
iteration-8-rl-environment
iteration-9-survival-reward
iteration-10-first-learning-fish
iteration-11-controlled-evaluation
iteration-12-multi-agent-learning
...
```

Suggested commit style:

```text
feat: add schooling state metrics
feat: model social predation risk
feat: add RL environment
feat: implement survival-driven reward
feat: train first learning fish
feat: add multi-agent learning
feat: add emergent schooling experiments
```

---

# Definition of success

SchoolMind is successful when the following sequence can be demonstrated experimentally:

```text
1. Start with hand-coded Boids schooling.

2. Introduce predator attacks.

3. Measure separation, alignment, cohesion,
   and individual social integration.

4. Establish that social state affects capture probability.

5. Create an RL environment where a fish can
   observe its local environment and act.

6. Train an individual fish using a primarily
   survival-driven reward.

7. Evaluate whether the learned fish becomes
   socially integrated while surviving.

8. Scale the problem to a school of learning agents.

9. Demonstrate whether collective schooling
   emerges from decentralized learning.

10. Measure the relationship between social
    integration and survival.

11. Test the result using controlled ablations
    and unseen environments.

12. Use the experiment framework to reproduce
    the findings.

13. Allow an AI research agent to formulate,
    run, analyze, and explain experiments.

14. Produce a research-style report grounded
    in actual simulation results.
```

The ultimate objective is therefore not simply:

> "Train fish to avoid predators."

It is:

> **Create an environment in which individual fish can discover through reinforcement learning that appropriate social organization improves survival, and investigate whether this local survival incentive is sufficient for collective schooling behavior to emerge.**

That distinction should remain the guiding principle for every stage after Iteration 5.