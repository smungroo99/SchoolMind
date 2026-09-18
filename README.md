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

# Iteration 6 — Quantify collective behavior

## Goal

Stop relying only on visual intuition.

Build measurable definitions of collective behavior.

### Metrics to explore

#### School cohesion

How tightly grouped are the fish?

#### Alignment

How similar are the fish headings?

#### Polarization

How strongly does the school move in one overall direction?

#### Dispersion

How spread out is the school?

#### Regrouping time

How long does it take for the school to return to a cohesive state after a predator disturbance? With multiple predators, record how this changes when threats are simultaneous or come from different directions.

#### Threat coverage

How much of the school is simultaneously within avoidance range of at least one predator? This helps distinguish a single localized threat from multi-directional pressure.

#### Survival

What proportion of fish survive each trial?

### Important

Define the metric mathematically in `docs/experiments.md` before implementing it.

### Deliverable

Plots such as:

- survival vs school size
- dispersion over time
- alignment over time
- predator distance over time
- regrouping time distributions

### Definition of done

You can describe what “better collective avoidance” means using measurable quantities without making a subjective judgment about the animation alone.

---

# Iteration 7 — Create the ML environment

## Goal

Convert the simulation into an environment suitable for reinforcement learning.

This is the major transition from simulation engineering into ML.

### First simplify the problem

Start with **one learning fish** in a school of rule-based fish.

The learning fish observes its local environment and learns to avoid one or more predators while remaining connected to the school.

### Observation space

A possible first observation vector:

```text
distance to nearest predator
relative direction to nearest predator
(optional) aggregated threat direction / strength from multiple predators
local average velocity
local school centroid direction
nearest-neighbor distance
nearest-neighbor relative velocity
own velocity
```

Do not make the observation space unnecessarily large at first.

### Action space

Start simple:

```text
turn left
turn right
maintain heading
accelerate
decelerate
```

Later you can move to continuous steering outputs.

### Deliverable

A functioning RL-compatible environment with reset/step behavior.

### Definition of done

You can run an agent through the environment and receive:

```text
observation → action → next observation → reward → done
```

---

# Iteration 8 — Reward engineering

## Goal

Design a reward function that expresses the behavior you want without explicitly programming the behavior itself.

### Possible reward components

Conceptually:

```text
+ staying alive
+ maintaining reasonable school proximity
+ maintaining useful alignment
+ increasing distance from immediate predator threat(s)
- being captured
- becoming completely isolated
- excessive unnecessary movement
```

### Critical lesson

Do not make the reward simply:

```text
reward = +1 if predator is far away
```

A poorly designed reward can produce unintended behavior.

For example, a fish could learn to permanently flee the school if survival dominates every other objective.

### Deliverable

Several reward designs with experiment results showing how behavior changes.

### Definition of done

You understand how reward shaping can create unintended incentives and can explain why the final reward was chosen.

---

# Iteration 9 — Train the first RL agent

## Goal

Train one fish to learn predator avoidance.

### Build

- neural-network policy
- rollout / experience collection
- reward tracking
- training loop
- model checkpointing
- evaluation mode

### Monitor

Track at minimum:

- episode reward
- survival time
- capture rate
- school distance
- training loss where appropriate

### Visualization

Create two modes:

```text
RULE-BASED
vs
RL AGENT
```

The learning agent should have a visible marker so you can identify it, and nearby predators should remain visually distinct.

### Deliverable

A trained model that can be loaded and evaluated without retraining.

### Definition of done

A reproducible command can train a model, save it, and later load it into the simulation.

### Git checkpoint

`iteration-9-first-rl-agent`

---

# Iteration 10 — Compare learned behavior with hand-coded behavior

## Goal

Build a proper evaluation framework.

### Compare

- hand-coded avoidance
- untrained random policy
- trained RL policy

Do not decide beforehand which approach will perform best. Let the experiment produce the measurements.

### Run controlled tests

Hold constant:

- school size
- predator speed
- simulation duration
- random seed sets

Vary only the policy.

### Deliverable

An evaluation report containing:

- survival metrics
- capture statistics
- school cohesion metrics
- plots
- example trajectories

### Definition of done

You can explain, using data, how learned behavior differs from the baseline behavior.

---

# Iteration 11 — Multi-agent reinforcement learning

## Goal

Make every sardine an autonomous learning agent.

This is where the original biological inspiration becomes the core ML challenge.

### Each fish gets

- local observation
- policy
- action
- reward
- state transition

The local observation must support multiple predators. A first implementation can expose the nearest predator, then later compare this with top-K predator observations or an aggregated threat representation.

### Important constraint

Initially keep communication implicit.

The agent should primarily observe nearby fish and predator state rather than receiving a centralized instruction such as “all fish disperse now.”

### Research question

Can decentralized local policies produce useful collective predator avoidance?

### Deliverable

A multi-agent environment in which all fish can learn.

### Definition of done

The simulation can run a school consisting entirely of learned agents.

---

# Iteration 12 — Study emergent behavior

## Goal

Investigate whether collective behaviors arise without directly programming them.

### Questions to test

- Do fish maintain a school under normal conditions?
- Does the school disperse when the predator approaches?
- Does the school regroup after the threat moves away?
- Does school size change the resulting behavior?
- Does local observation lead to useful group-level coordination?
- What happens when communication / observation is restricted?

### Compare

Create controlled variants such as:

```text
A. rule-based fish
B. individually trained fish
C. jointly trained multi-agent school
D. limited-observation agents
```

### Deliverable

A research-style experiment report with visual demonstrations and quantitative metrics.

---

# Iteration 13 — Generalization tests

## Goal

Determine whether the agents learned a narrow trick or a more general strategy.

Train under one set of conditions.

Evaluate under unseen conditions.

### Example

Train:

```text
school size: 100
predator speed: 1.5
predator count: 1
```

Evaluate on:

```text
school size: 50
school size: 200
predator speed: 1.2
predator speed: 1.8
predator count: 2 or 3
multiple predators with different spawn patterns
```

### Why this matters

A model that only succeeds under its training conditions may be overfitting the environment.

### Deliverable

A generalization matrix showing training and evaluation conditions.

---

# Iteration 14 — Experiment automation

## Goal

Make the simulator usable as a research tool rather than a single demo.

### Create tools/functions such as

```text
create_scenario()
run_trial()
run_batch()
load_model()
evaluate_model()
compare_models()
configure_predators()
calculate_metrics()
generate_report()
```

### Example experiment request

```text
Run 100 trials for school sizes 25, 50, 100 and 200.
Keep predator speed fixed and repeat the experiment with 1, 2 and 3 predators.
Report survival rate, first-capture time,
and regrouping time.
```

The system should be able to execute this reproducibly without manually changing source code.

### Deliverable

A command-line experiment API or Python interface.

---

# Iteration 15 — Hugging Face AI Agent integration

## Goal

Connect the project to what you are learning in the Hugging Face AI Agents course.

The LLM does **not** control every sardine directly.

Instead, the LLM becomes a **researcher/operator** that uses tools exposed by the SchoolMind experiment framework.

### Example tools

```python
run_simulation(...)
run_batch_experiment(...)
configure_predators(...)
get_metrics(...)
compare_runs(...)
plot_result(...)
load_experiment(...)
```

### Example user interaction

```text
User:
Investigate how school size and predator count affect survival.

Research Agent:
I will test school sizes 25, 50, 100 and 200 across 1, 2 and 3 predators.

→ creates experiment
→ runs trials
→ retrieves results
→ analyzes metrics
→ identifies notable patterns
→ generates report
```

### Key principle

The LLM should use deterministic tools for computation.

Do **not** ask the LLM to invent numerical results or perform the simulation inside its context window.

The simulation engine generates the data.
The analysis code calculates the metrics.
The LLM interprets and communicates the results.

### Deliverable

A working AI researcher that can operate the experiment framework through tools.

### Git checkpoint

`iteration-15-ai-researcher`

---

# Iteration 16 — Research memory and experiment history

## Goal

Allow the AI researcher to keep track of previous experiments.

### Store

- experiment configuration
- random seeds
- model used
- metrics
- plots
- timestamps
- research question
- generated summary

### Example

```text
Experiment #042
Question: Does increasing school size improve survival?
School sizes: 25, 50, 100, 200
Predator speed: 1.5
Trials per condition: 100
Model: MARL-v3
```

The agent should be able to refer to previous experiments by ID.

### Deliverable

A lightweight experiment registry stored locally in a database or structured files.

---

# Iteration 17 — Visual research dashboard

## Goal

Turn the project into a polished interactive application.

### Dashboard sections

#### Simulation

- live animation
- play/pause/reset
- speed control
- scenario selector
- predator count / predator configuration
- model selector

#### Metrics

- survival rate
- capture rate
- school cohesion
- alignment
- dispersion
- regrouping time

#### Experiments

- create experiment
- run batch
- compare runs
- inspect trajectories

#### AI Researcher

- natural-language research request
- tool execution log
- experiment summaries
- generated reports

### Deliverable

A single interface that can demonstrate the whole project.

---

# Iteration 18 — Final portfolio polish

## Goal

Make SchoolMind presentable as a serious portfolio project.

### README should include

1. Project motivation
2. Biological inspiration
3. Architecture diagram
4. Simulation screenshots / GIFs
5. ML methodology
6. Reward design
7. Multi-agent setup
8. Experiment methodology
9. Results
10. AI researcher architecture
11. How to run locally
12. Future research directions

### Add

- architecture diagram
- example videos/GIFs
- reproducible experiments
- configuration examples
- training instructions
- evaluation instructions
- clean logging
- meaningful tests

### Deliverable

Someone should be able to clone the repository, follow the README, and understand both **what the project does** and **why the architecture works that way**.

---

# 7. Suggested milestone timeline

Do not treat these as deadlines. They are sequencing guidance.

```text
FOUNDATION
│
├── 0. VS Code + Python setup
├── 1. Basic simulation
├── 2. Fish physics
│
▼
EMERGENT BEHAVIOR
│
├── 3. Boids schooling
├── 4. Predator
├── 5. Experiment framework
├── 6. Behavior metrics
│
▼
MACHINE LEARNING
│
├── 7. RL environment
├── 8. Reward design
├── 9. First RL agent
├── 10. Evaluation
│
▼
MULTI-AGENT AI
│
├── 11. Multi-agent RL
├── 12. Emergent behavior studies
├── 13. Generalization
├── 14. Experiment automation
│
▼
LLM AGENTS
│
├── 15. Hugging Face AI researcher
├── 16. Experiment memory
├── 17. Visual dashboard
│
▼
PORTFOLIO
│
└── 18. Documentation + polish
```

---

# 8. Parallel Hugging Face AI Agents learning track

Run the Hugging Face course **in parallel**, but do not force every lesson into SchoolMind immediately.

The idea is:

```text
Hugging Face course concept
          ↓
understand it in isolation
          ↓
ask: "Can SchoolMind use this?"
          ↓
implement only when useful
```

A sensible mapping is:

| AI Agent concept | SchoolMind application |
|---|---|
| Agent loop | Researcher repeatedly performs experiment tasks |
| Tools | Run simulation / retrieve metrics / compare runs |
| Tool schemas | Formal experiment-tool interface |
| Planning | Break research questions into experiments |
| Tool calling | Execute simulation framework |
| Memory | Recall prior experiments |
| Multi-step reasoning | Decide what experiment to run next |
| Structured outputs | Produce machine-readable experiment summaries |
| Evaluation | Measure how well the researcher completes tasks |

The simulation and ML environment should remain usable **even if the LLM layer is completely removed**.

---

# 9. First project questions to investigate

Once the core simulator exists, start thinking like a researcher.

Possible research questions:

### School size

Does changing the number of fish change predator-avoidance outcomes?

### Predator speed

How sensitive is collective behavior to predator speed?

### Number of predators

How does increasing predator count change school dispersion, survival, and regrouping?

### Predator geometry

Does the direction and spatial arrangement of multiple predators matter more than predator count alone?

### Predator coordination

How do independently hunting predators compare with explicitly coordinated predator strategies?

### Observation radius

How much local information does each fish need?

### School cohesion

Is there a tradeoff between staying tightly grouped and escaping a predator?

### Multi-agent learning

Can decentralized agents develop coordinated behavior without explicit communication?

### Generalization

Do policies trained in one environment transfer to different conditions?

### Energy cost

Can agents survive while minimizing unnecessary movement?

Do not try to answer all of these at once. Each one can become its own controlled experiment.

---

# 10. What NOT to do early

Avoid the following during the first iterations:

- Do not begin with a complicated deep-learning architecture.
- Do not add an LLM before the simulation works.
- Do not build a web frontend immediately.
- Do not use a huge observation vector “just in case.”
- Do not make the reward function extremely complicated on the first RL attempt.
- Do not run massive training jobs before validating the environment.
- Do not judge a policy from a single simulation.
- Do not rely entirely on visual inspection for model evaluation.

The project should become more sophisticated gradually.

---

# 11. Reproducibility requirements

From the experiment stage onward, every run should record:

```text
experiment_id
random_seed
school_size
predator_count
predator_speed
predator_spawn_pattern
predator_behavior / coordination mode
simulation_duration
behavior_model
RL_model/checkpoint
reward configuration
environment configuration
metrics
```

A result should always be traceable back to the exact conditions that produced it.

This is especially important once the AI researcher begins creating experiments automatically.

---

# 12. Testing strategy

Write tests continuously rather than waiting until the end.

### Unit tests

Examples:

```text
Fish position updates correctly.
Velocity never exceeds the configured maximum.
Separation produces a repulsive steering vector.
Capture occurs within the correct radius.
Metrics are calculated correctly.
Random seeds produce reproducible results.
```

### Integration tests

Examples:

```text
Simulation can start and finish.
Batch runner creates N trials.
Model can be loaded into the environment.
AI researcher can call a simulation tool.
```

### ML evaluation tests

Examples:

```text
Training does not crash.
Checkpoints can be saved and restored.
Evaluation can run without exploration noise when desired.
```

---

# 13. Suggested Git workflow

Use a simple branch/commit structure.

```text
main
│
├── iteration-1-basic-simulation
├── iteration-2-fish-physics
├── iteration-3-emergent-schooling
├── iteration-4-predator
├── iteration-5-experiment-framework
...
```

You do not have to create a long-lived branch for every iteration. The important part is maintaining clear checkpoints.

Suggested commit style:

```text
feat: add fish steering physics
feat: implement boids schooling
feat: add predator tracking
feat: add experiment batch runner
feat: add RL environment
feat: add research agent tools
```

---

# 14. Definition of success

The project is successful when you can demonstrate the following sequence:

```text
1. Show the original rule-based school.

2. Introduce one predator, then switch to multiple predators using configuration only.

3. Show the school dispersing / avoiding the predators.

4. Explain exactly how the rule-based behavior works.

5. Replace hand-coded behavior with learned agents.

6. Train and evaluate the agents.

7. Show what behavior emerges.

8. Run controlled experiments.

9. Ask the AI researcher a natural-language research question.

10. Watch it configure and run experiments using tools.

11. Inspect the resulting metrics and visualizations.

12. Read a generated research-style summary grounded in the actual results.
```

That is the point at which SchoolMind becomes much more than a simulation: it becomes a small **multi-agent AI experimentation platform**.

---

# 15. Our working method for building it together

For each iteration, use this sequence:

```text
YOU
↓
Open VS Code
↓
Create/modify the files for the iteration
↓
Run the project
↓
Observe the result
↓
Bring errors / screenshots / behavior back
↓
WE debug and improve
↓
Commit the iteration
↓
Move to the next concept
```

When we work on an iteration together, prioritize understanding over copy/paste. For major ML components, I should explain:

- what the component does
- why it exists
- what data enters it
- what comes out
- how it is trained
- what assumptions it makes
- how we evaluate whether it works

---

# 16. First concrete build target

Do **not** start by implementing the entire repository.

The first coding milestone should be:

```text
SchoolMind v0.1

✓ VS Code project
✓ Python virtual environment
✓ Git repository
✓ Pygame window
✓ 50–100 fish
✓ 1+ configurable predators (start with 1)
✓ Fish position + velocity
✓ Basic rendering
✓ Run / pause / reset
✓ Clean simulation loop
```

Once that runs correctly, move immediately to Iteration 2.

The first meaningful visual goal is simply:

> **Open VS Code → run one command → see a school of fish moving around on screen.**

Everything else builds on that foundation.

### Multi-predator sanity check

Before starting reinforcement learning, make one quick configuration change:

```yaml
predator_count: 2
```

The simulation should still run without code changes. Later, the same switch should support 3, 5, or more predators. This small architectural constraint will prevent us from having to redesign the environment when we reach the harder multi-agent experiments.
