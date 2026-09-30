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

# Iteration 7 — Build the social predation-risk mechanism

## Goal

Introduce the central environmental mechanism required for the eventual SchoolMind research question:

> **Can decentralized fish learn collective schooling behavior because local social organization changes their probability of surviving predation?**

The purpose of this iteration is **not** to teach fish to school and not to create a predator that explicitly prefers or avoids schools.

Instead, the environment should create a plausible and measurable relationship between:

```text
fish movement
     ↓
local social configuration
     ↓
predator interaction
     ↓
capture probability
     ↓
survival
```

This is the critical bridge between the hand-coded simulation and the future reinforcement-learning problem.

---

## Central research hypothesis

The long-term hypothesis is:

> **Individual fish can discover movement strategies that improve survival under predation, and when all fish learn from local observations, this may produce emergent schooling behavior without an explicit schooling reward.**

The project should therefore avoid directly rewarding or commanding schooling.

We should not tell an agent:

```text
"Move toward the school."
"Stay within X pixels of the centroid."
"Maintain exactly 5 neighbors."
```

Instead, the environment should make some local social configurations more advantageous than others.

---

## Design principle: model vulnerability, not "school membership"

The predator should not first determine:

```text
"This fish is in a school."
```

and then apply a school bonus.

That would make schooling a predefined category rather than an emergent outcome.

Instead, capture risk should depend on **local interaction and exposure**.

The initial model should consider mechanisms such as:

```text
isolation / dilution
        +
local exposure / edge position
        +
predator target ambiguity
        +
excessive local crowding
```

These mechanisms can interact to create a region of lower vulnerability without defining one exact geometric shape as "the school."

---

## 1. Dilution

An isolated fish has fewer nearby alternative prey.

Conceptually:

```text
isolated fish
     ↓
few nearby prey
     ↓
little dilution
     ↓
higher individual vulnerability
```

A fish surrounded by multiple nearby prey has more potential targets in its local neighborhood.

The initial implementation should remain simple and stochastic rather than assuming an exact biological formula.

---

## 2. Predator confusion

A predator encountering several nearby fish that are moving in similar ways should have greater difficulty successfully selecting and tracking one individual.

Conceptually:

```text
few nearby comparable fish
        ↓
low target ambiguity
        ↓
higher capture success


many nearby comparable fish
        ↓
greater target ambiguity
        ↓
lower capture success
```

A first computational approximation can use local prey count and movement similarity as inputs.

The model should represent **target ambiguity**, not a direct "school score."

---

## 3. Local exposure / edge position

A fish surrounded by neighbors may have greater protection than a fish exposed on the outside of a group.

Conceptually:

```text
        predator
           ↓

      🐟  🐟  🐟
    🐟  🐟  🐟  🐟
       🐟  🐟

      interior
        ↑
   more surrounded


      🐟
   exposed edge
        ↑
     greater
     exposure
```

This provides an important mechanism through which an individual can benefit from moving toward other fish without the simulation explicitly telling it to form a school.

---

## 4. Excessive crowding

Grouping should not automatically mean:

```text
more fish nearby = always better
```

Extremely tight configurations can introduce another form of vulnerability, such as reduced maneuverability or local interference.

Conceptually:

```text
very isolated
     ↓
higher vulnerability

reasonable local spacing
     ↓
lower vulnerability

extremely crowded
     ↓
higher vulnerability
```

This creates a potential **intermediate region of lower risk** rather than rewarding infinite density.

The exact relationship should be treated as an experimental modeling assumption and validated empirically.

---

## Combined vulnerability model

The initial capture mechanism can be represented conceptually as:

```text
baseline predator capture risk
                ×
       social vulnerability
                ↓
        capture probability
```

The social vulnerability term can be influenced by:

```text
local prey density
local spacing
local movement similarity
local exposure
local crowding
```

The exact mathematical function should be kept simple initially.

The first version should produce a **bounded stochastic modifier**, not deterministic protection.

For example:

```text
low vulnerability
        ↕
normal vulnerability
        ↕
high vulnerability
```

A well-positioned fish can still be captured.

An isolated fish can still survive.

The difference should emerge statistically across many trials.

---

## Important constraint: do not hard-code "the school"

Do not implement:

```text
if fish_in_school:
    capture_probability *= 0.5
```

or:

```text
if neighbor_count > 5:
    fish_is_safe = True
```

These approaches would directly encode the desired behavior.

Instead, use the underlying local quantities already measured by Iteration 6:

```text
neighbor_count
nearest_neighbor_distance
mean_neighbor_distance
alignment
cohesion_distance
```

and, where useful, derive additional predator-relative quantities such as local exposure or target ambiguity.

The environment should never need a perfect binary definition of:

```text
school / not school
```

in order to create the survival pressure.

---

## One large school vs many small schools

Do **not** initially impose:

```text
one large school = bad
many small schools = good
```

as an explicit global rule.

The first mechanism should primarily operate on the **local environment around an individual fish**.

A large school may provide more nearby alternatives and greater target ambiguity, while also potentially being more detectable or locally crowded.

Several smaller schools may produce different local conditions.

Those outcomes should be **measured**, not assumed.

Later experiments can compare:

```text
one large school
vs
several medium schools
vs
many small schools
```

using the cluster metrics already available from Iteration 6.

This makes school structure an experimental result rather than a scripted objective.

---

## Keep predator behavior simple initially

The predator does not need to become an intelligent "school hunter."

The initial predator should remain close to the established baseline:

```text
random spawn
     ↓
detect nearby fish
     ↓
select target
     ↓
pursue
     ↓
attempt capture
```

Nearest-fish targeting can remain the baseline target-selection mechanism.

The major change in Iteration 7 is the **probability of successful capture once a predator interacts with a fish**, not a complete redesign of predator intelligence.

This separation is important because it lets us test whether the social-risk mechanism itself produces the intended learning signal.

---

## Validation before reinforcement learning

Before introducing RL, the environment must be tested using the current rule-based fish.

The goal is to establish:

> **Does local social configuration measurably affect individual predation outcomes?**

Controlled experiments should create or identify fish experiencing different local states, such as:

```text
isolated
lightly grouped
well surrounded
poorly aligned
extremely crowded
```

Then measure:

```text
capture probability
time to capture
survival time
local social metrics
predator exposure
```

The important relationship is:

```text
local social state at time t
             ↓
predation risk during t → t + Δt
             ↓
capture / survival
```

This should be analyzed using repeated randomized trials rather than individual anecdotes.

---

## What Iteration 7 must demonstrate

We are **not** trying to prove a biological law.

We are trying to verify that our computational environment contains a useful causal learning signal.

A successful result would look approximately like:

```text
different local social configurations
                ↓
different average capture probabilities
```

while avoiding:

```text
school → safe
not school → dead
```

The relationship should remain probabilistic and imperfect.

---

## Research constraint

The mechanism must be:

```text
strong enough
     ↓
for RL to learn from survival differences
```

but:

```text
not so explicit
     ↓
that schooling is directly scripted
```

We want:

```text
local interactions
      ↓
different predation outcomes
      ↓
survival differences
      ↓
learning signal
      ↓
possible emergent schooling
```

not:

```text
schooling rule
      ↓
schooling behavior
```

---

## Deliverable

A validated baseline predation-risk model in which local social and predator-relative conditions measurably influence individual capture probability.

### Definition of done

Across repeated controlled trials:

* the same predator and world conditions can produce different capture rates under different local social configurations
* capture remains probabilistic
* the predator does not require an explicit "school" classifier
* the mechanism does not directly reward or command schooling
* the experiment framework records enough information to analyze social state immediately before capture

### Git checkpoint

`iteration-7-social-predation-risk`

---

# Iteration 8 — Build the reinforcement-learning environment

## Goal

Convert the validated simulation into an RL environment while preserving the separation between:

```text
simulation
behavior
observation
reward
training
```

The environment should expose local information to individual agents and allow them to experience the consequences of their actions.

---

## First learning setup

Do not make every fish learn immediately.

Start with:

```text
1 learning fish
+
rule-based fish
+
1 predator
```

The rest of the population continues using the established Boids behavior.

This provides a controlled environment in which we can determine whether one learning fish can discover useful predator-avoidance behavior before introducing full multi-agent learning.

---

## Observation design

The learning fish should receive information that could reasonably be available to an individual fish.

A first observation could contain:

```text
own velocity
nearest-neighbor distance
local neighbor count
local average neighbor direction
local cohesion information
local spacing information
nearest predator distance
nearest predator relative direction
```

Additional local predator information can be added later when necessary.

The important principle is:

```text
local observation
```

rather than:

```text
global instruction
```

For example:

```text
DO NOT:
"the school contains 64 fish"

PREFER:
"I have 7 nearby fish"
```

The observation space should remain deliberately small.

---

## Action space

Begin with a simple action space such as:

```text
turn left
maintain heading
turn right
accelerate
decelerate
```

Continuous steering can be introduced later.

---

## Environment interface

Implement a standard interface:

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

A functioning RL environment capable of running a random policy from start to finish.

### Definition of done

A learning fish can interact with the existing simulation and receive valid observations, actions, rewards, and termination signals without requiring a complete RL training system.

### Git checkpoint

`iteration-8-rl-environment`

---

# Iteration 9 — Design a survival-driven reward

## Goal

Design the reward so that fish are rewarded for **survival**, not for explicitly performing schooling behavior.

This is one of the most important design constraints in the entire project.

---

## Primary principle

The central objective is:

> **Schooling should emerge because collective social behavior improves survival, not because the reward explicitly tells fish to school.**

Therefore, the first reward should remain deliberately simple.

Conceptually:

```text
small positive reward for surviving
+
large negative reward for capture
```

The schooling signal should arise indirectly:

```text
movement choice
      ↓
local social configuration
      ↓
different capture probability
      ↓
different expected survival
      ↓
different long-term reward
```

---

## Avoid explicit schooling rewards

Do not initially use:

```text
+ alignment
+ cohesion
+ separation
+ school membership
+ distance to school centroid
+ number of neighbors
```

as direct reward terms.

For example:

```text
reward += cohesion
```

would explicitly teach the agent that cohesion is desirable.

That would make it difficult to determine whether schooling emerged from survival pressure or simply from the reward function.

---

## Reward validation

Before long training runs, test the reward with simple policies.

Compare:

```text
random policy
rule-based policy
simple heuristic policies
```

Track:

```text
episode reward
survival time
capture rate
social metrics
school metrics
```

The purpose is to detect unintended incentives.

For example, a policy that survives by permanently escaping the fish population would require investigation even if its reward is high.

---

## Deliverable

A documented survival-oriented reward formulation with short validation experiments.

### Definition of done

The reward is mathematically understandable, reproducible, and does not directly encode "form a school" as its primary objective.

### Git checkpoint

`iteration-9-survival-reward`

---

# Iteration 10 — Train the first learning fish

## Goal

Train one learning fish to survive inside the existing rule-based population.

The first question is:

> **Can an individual fish learn movement behavior that improves survival when local social configuration affects predation risk?**

---

## Training setup

Start with:

```text
1 learning fish
+
rule-based fish
+
1 predator
```

The rule-based population provides a moving social environment.

The learning fish must discover how to move within that environment while experiencing the survival consequences of its actions.

---

## Build

Implement:

```text
policy network
experience collection
training loop
checkpointing
evaluation mode
deterministic evaluation seeds
```

---

## Monitor

Track at minimum:

```text
episode reward
survival time
capture rate
neighbor count
neighbor distances
alignment
cohesion
social integration / cluster participation
predator exposure
```

The key question is not simply:

```text
Did reward increase?
```

It is:

```text
Did survival improve because the fish learned
a useful interaction with the surrounding population?
```

---

## Watch for shortcut strategies

A learned fish could discover a strategy that improves survival without contributing to the eventual research question.

Examples include:

```text
always flee from every fish
remain near a boundary
exploit a simulation artifact
avoid all predator interactions by leaving the population
```

These behaviors should be identified rather than automatically considered successful.

---

## Deliverable

A reproducible trained policy for one learning fish that can be evaluated independently of training.

### Git checkpoint

`iteration-10-first-learning-fish`

---

# Iteration 11 — Controlled evaluation of the learned strategy

## Goal

Determine what the first learning agent actually learned.

Do not assume that higher survival means successful social predator avoidance.

---

## Compare policies

Run controlled evaluations of:

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
capture probability
neighbor count
neighbor distances
alignment
cohesion
cluster participation
predator distance
```

---

## Causal analysis

The most important analysis is:

```text
local social state at time t
             ↓
capture probability after t
```

This allows us to distinguish:

```text
"the fish survived"
```

from:

```text
"the fish survived while using
the social environment effectively"
```

---

## Counterfactual evaluation

Where practical, evaluate the learned policy under altered environmental mechanisms:

```text
normal social-risk mechanism
vs
reduced social-risk mechanism
vs
no social-risk mechanism
```

If the learned behavior only works when the intended social mechanism exists, that provides stronger evidence that the environment is actually producing the intended learning problem.

---

## Ablation of observations

Remove selected observation components:

```text
without neighbor information
without alignment information
without cohesion information
without spacing information
```

Then evaluate how behavior changes.

This helps determine whether the learned policy is actually using local social information.

---

## Deliverable

A quantitative evaluation of the first learned behavior and evidence about whether it is exploiting local social interactions rather than a simulation artifact.

### Git checkpoint

`iteration-11-controlled-learning-evaluation`

---

# Iteration 12 — Multi-agent reinforcement learning

## Goal

Move from one learning fish to a population in which **all fish are learning agents**.

This is where decentralized learning becomes the central experiment.

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

Start with parameter sharing:

```text
Fish 1 ─┐
Fish 2 ─┤
Fish 3 ─┼──→ shared policy
Fish 4 ─┤
Fish N ─┘
```

Each fish still receives its own local observation and selects its own action.

The agents therefore remain decentralized even though they may share policy parameters.

---

## No explicit communication

Do not provide messages such as:

```text
"move toward the center"
"everyone turn left"
"the school is under attack"
```

Coordination should emerge from:

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

Begin with the simplest case:

```text
1 predator
```

Then evaluate:

```text
2 predators
3+ predators
```

using the multi-predator capabilities already present in the simulation.

---

## Deliverable

A simulation in which the entire fish population consists of learning agents operating from local information.

### Definition of done

The learned population can repeatedly interact with predators without relying on hand-coded Boids rules for movement.

### Git checkpoint

`iteration-12-multi-agent-learning`

---

# Iteration 13 — Test whether schooling emerges

## Goal

This is the central scientific evaluation of SchoolMind.

The question is:

> **Can decentralized fish agents develop schooling behavior because social organization improves individual survival?**

---

## Primary hypothesis

The hypothesis is not:

```text
"fish will definitely form a school."
```

It is:

> **When local social organization changes predation risk and agents optimize survival from local observations, collective schooling behavior may emerge.**

Possible outcomes include:

```text
strong schooling
partial schooling
multiple schools
different collective behavior
weak coordination
failure to school
```

All outcomes are informative.

---

## Compare

Evaluate:

```text
A. rule-based Boids population
B. independently trained learning fish
C. fully learned multi-agent population
```

Where useful, also evaluate:

```text
D. learned agents with restricted social observations
```

---

## Key measurements

Measure both individual and population behavior:

```text
survival rate
capture probability
survival time
neighbor count
neighbor distances
alignment
cohesion
cluster count
school count
school fish fraction
largest cluster fraction
cluster polarization
cluster dispersion
global population metrics
regrouping time
```

---

## Most important analysis

Analyze the relationship:

```text
local social state at time t
             ↓
predation probability
             ↓
survival
```

and separately:

```text
local decisions
      ↓
population-wide organization
      ↓
school formation / maintenance
```

This lets us distinguish a genuinely emergent collective behavior from an agent that merely learned to escape predators individually.

---

## Emergence criteria

A learned population should not be called "schooling" simply because the fish occasionally become close.

Evidence should involve multiple measurements, such as:

```text
persistent local connectivity
+
reasonable spacing
+
coordinated movement
+
repeatable collective structure
```

The existing Iteration 6 metrics should provide the quantitative basis for this evaluation.

---

## Deliverable

A research-style analysis answering:

> **Did schooling emerge from survival-driven decentralized learning?**

The analysis should include:

```text
quantitative results
+
time-series plots
+
individual capture analysis
+
visual examples of learned behavior
```

### Git checkpoint

`iteration-13-emergent-schooling`

---

# Iteration 14 — Ablation, robustness, and generalization

## Goal

Determine whether the learned behavior depends on the intended social-predation mechanism or exploits an accidental feature of the simulation.

---

## Environment ablations

Test variants such as:

```text
A. full social-risk mechanism

B. no dilution/confusion effect

C. no local exposure effect

D. no crowding effect

E. no social-risk mechanism
```

The purpose is to determine which environmental mechanisms are actually responsible for the learned behavior.

---

## Observation ablations

Also test:

```text
without neighbor observations
without alignment information
without cohesion information
without spacing information
```

This separates:

```text
environmental cause
```

from:

```text
information available to the agent
```

---

## Generalization

Train under one set of conditions and evaluate under unseen conditions.

For example:

```text
TRAIN
fish count: 75
predator count: 1
predator speed: baseline
capture cooldown: baseline
```

Then evaluate under:

```text
different fish counts
2 predators
different predator speeds
different capture cooldowns
independent vs coordinated predators
```

The goal is to determine whether the learned strategy represents a general behavioral pattern or a narrow solution to one exact environment.

---

## Deliverable

A controlled ablation and generalization matrix showing how learned behavior changes when the environment or available information is modified.

### Git checkpoint

`iteration-14-ablation-generalization`

---

# Iteration 15 — Build the experiment and evaluation interface

## Goal

Turn the experiment framework into a reusable research API capable of comparing:

```text
policies
environment mechanisms
training configurations
predator scenarios
```

without modifying simulation source code for every experiment.

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
```

across:

```text
different fish populations
1, 2, and 3 predators
different predator speeds
different coordination modes
different social-risk mechanisms
```

and report:

```text
survival
capture probability
social organization
cluster structure
alignment
cohesion
dispersion
```

The reproducibility system established earlier should remain the foundation.

---

## Deliverable

A reusable evaluation layer that allows experiments to be defined without modifying the underlying simulation implementation.

---

# Iteration 16 — Hugging Face AI Researcher

## Goal

Connect SchoolMind to the AI-agent concepts being learned in parallel.

The LLM should **not control individual fish**.

Instead, it becomes a research assistant that operates the experiment framework.

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

A future user could ask:

```text
Investigate whether the relationship between
local social organization and survival changes
when predator density increases.
```

The researcher could:

```text
define experiment
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

The LLM must never invent numerical results.

The deterministic SchoolMind system should:

```text
run simulation
calculate metrics
produce results
```

while the researcher:

```text
interprets
compares
explains
communicates
```

those results.

### Git checkpoint

`iteration-16-ai-researcher`

---

# Iteration 17 — Research memory and visual dashboard

## Goal

Give SchoolMind a polished research interface and persistent experiment history.

The final system should make it easy to:

```text
create experiments
run experiments
inspect results
compare policies
visualize schooling
review previous findings
```

---

## Experiment history

Each experiment should retain:

```text
experiment configuration
random seeds
simulation parameters
policy/model information
trial-level results
social time series
individual social measurements
capture events
plots
analysis
```

This allows previous experiments to be reproduced and compared.

---

## Visual dashboard

The final interface can expose:

```text
LIVE SIMULATION
    ↓
population metrics
    ↓
school / cluster structure
    ↓
capture events
    ↓
individual fish analysis
    ↓
experiment comparison
    ↓
AI researcher
```

Useful visualizations may include:

```text
survival curves
capture probability by social state
cluster size distributions
alignment over time
neighbor-distance distributions
school formation over time
individual trajectories
predator trajectories
```

---

## Final research loop

The completed SchoolMind system should support:

```text
research question
      ↓
hypothesis / experiment design
      ↓
simulation
      ↓
repeated trials
      ↓
metrics
      ↓
statistical / visual analysis
      ↓
interpretation
      ↓
new experiment
```

The long-term goal is not merely to produce fish that look like they are schooling.

The goal is to create a **research system in which schooling can emerge from decentralized survival-driven learning and then be quantitatively investigated.**
