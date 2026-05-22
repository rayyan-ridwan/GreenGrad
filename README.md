# 🌱 GreenGrad

GreenGrad is an energy-aware training helper for machine learning projects.  
It helps you monitor training resource usage, apply sustainability policies,
and generate simple reports so teams can reduce energy waste while iterating.

## Why GreenGrad?

Modern model training can be resource intensive. GreenGrad provides a lightweight
foundation to:

- Track CPU/RAM/GPU-related metrics during training
- Flag budget violations (for example, max power limits)
- Produce quick markdown reports to review training efficiency

## Project Status

GreenGrad is in early development. The current version establishes core
building blocks for:

- Resource metric snapshots
- Policy checks (for sustainability budgets)
- Basic reporting utilities
- A minimal trainer loop abstraction

## Repository Structure

```text
GreenGrad/
├── greengrad/
│   ├── __init__.py
│   ├── policy.py
│   ├── report.py
│   ├── tracker.py
│   └── trainer.py
├── tests/
│   ├── test_policy.py
│   ├── test_report.py
│   ├── test_tracker.py
│   └── test_trainer.py
├── notebook_examples/
│   └── README.md
├── requirements.txt
└── README.md
```

## Quick Start

### 1) Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

### 3) Run tests

```bash
python -m unittest discover -s tests -p "test*.py"
```

## Example Usage

```python
from greengrad import ResourceTracker, EnergyBudgetPolicy, SustainableTrainer

def metrics_provider():
    return {
        "cpu_percent": 42.0,
        "ram_percent": 58.0,
        "gpu_power_watts": 210.0,
        "gpu_utilization_percent": 77.5,
    }

tracker = ResourceTracker(metrics_provider=metrics_provider)
policy = EnergyBudgetPolicy(max_power_watts=220.0)
trainer = SustainableTrainer(tracker=tracker, policy=policy)

def train_step(step, snapshot):
    # place your model training step logic here
    return {"step": step, "power": snapshot.gpu_power_watts}

results = trainer.run(steps=3, step_fn=train_step)
print(results)
```

## Development Roadmap

- [x] Define initial project structure
- [x] Implement core tracking/policy/report modules
- [x] Add baseline unit tests
- [ ] Add optional integrations for PyTorch and TensorFlow
- [ ] Add richer visualization and experiment comparison dashboards
- [ ] Add CLI and config-driven execution mode

## Contributing

Contributions are welcome. For now:

1. Open an issue describing your idea/bug.
2. Add focused changes with tests.
3. Keep the sustainability focus in mind: optimize both model quality and
   resource impact.

---

Built for greener machine learning workflows.
