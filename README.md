# SchoolMind

SchoolMind is a Python-based multi-agent predator/prey simulation project inspired by sardine schools.

## Iteration 0: Development environment

This repository sets up the first working Python project structure for SchoolMind so it can be developed and run from VS Code.

## Project structure

```text
SchoolMind/
├── .venv/
├── .vscode/
├── src/
│   └── schoolmind/
├── tests/
├── .env.example
├── .gitignore
├── README.md
├── pyproject.toml
└── SchoolMind_Project_Plan.md
```

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
python -m schoolmind
```

## Running tests

```bash
pytest
```

## Notes

This repository intentionally starts small and keeps the structure ready for later iterations involving fish simulation, boids behavior, predators, experiments, and ML.
