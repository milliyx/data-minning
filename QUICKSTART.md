# Quick Start Guide

Get up and running with the MD Lakehouse template in 5 minutes!

## Prerequisites

- Python 3.11 or higher
- Git
- 4GB RAM minimum (8GB recommended)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/mineria-datos-lakehouse-template.git
cd mineria-datos-lakehouse-template
```

### 2. Install Dependencies

**Option A: Using Make (recommended)**
```bash
make setup
```

**Option B: Using pip directly**
```bash
pip install -e ".[dev]"
```

This installs:
- PySpark 3.5.0
- scikit-learn
- pandas, numpy
- Testing tools (pytest, ruff)
- And all other dependencies

## First Run

### Run Complete Pipeline

```bash
make all TEAM=configs/teams/team01.yaml RUN_DATE=2026-02-01
```

This command will:
1. ✅ Generate Bronze data (raw simulation)
2. ✅ Run Bronze→Silver pipeline (cleaning + validation)
3. ✅ Run Silver→Gold pipeline (analytics + features)
4. ✅ Build ML features
5. ✅ Train 3 models (churn, LTV, segmentation)
6. ✅ Generate evaluation report

**Expected runtime**: 3-5 minutes (depends on your CPU)

### Verify Success

After completion, you should see:

```
data/
├── bronze/
│   ├── users/
│   ├── subscriptions/
│   ├── payments/
│   ├── usage_logs/
│   └── events/
├── silver/        (same tables, cleaned)
├── gold/          (analytics tables)
├── models/        (*.json metrics files)
└── reports/       (evaluation_report_*.md)
```

## Explore Results

### 1. Check Model Metrics

```bash
# View churn model results
cat data/models/churn_metrics_2026-02-01.json

# View evaluation report
cat data/reports/evaluation_report_2026-02-01.md
```

### 2. Open Jupyter Notebooks

```bash
jupyter notebook notebooks/
```

Start with:
- `00_intro.ipynb` - Course introduction
- `01_kdd.ipynb` - KDD process explained
- `02_etl.ipynb` - ETL pipeline walkthrough
- `03_models.ipynb` - Model training and evaluation

### 3. Query Data with PySpark

```python
from pyspark.sql import SparkSession
from pathlib import Path

spark = SparkSession.builder.appName("exploration").getOrCreate()

# Read users table
users = spark.read.parquet("data/bronze/users/run_date=2026-02-01")
users.show()

# Check churn features
churn_features = spark.read.parquet("data/gold/churn_features/run_date=2026-02-01")
churn_features.describe().show()
```

## Step-by-Step Execution

If you prefer to run each step individually:

```bash
# 1. Generate Bronze data
python -m md_lakehouse.cli generate --team configs/teams/team01.yaml --run-date 2026-02-01

# 2. Run ETL pipeline
python -m md_lakehouse.cli pipeline --team configs/teams/team01.yaml --run-date 2026-02-01

# 3. Build features
python -m md_lakehouse.cli features --team configs/teams/team01.yaml --run-date 2026-02-01

# 4. Train models
python -m md_lakehouse.cli train --team configs/teams/team01.yaml --run-date 2026-02-01

# 5. Evaluate
python -m md_lakehouse.cli evaluate --team configs/teams/team01.yaml --run-date 2026-02-01
```

## Customize Your Team

### Create Your Team Config

```bash
cp configs/teams/team01.yaml configs/teams/my_team.yaml
```

Edit `my_team.yaml`:

```yaml
team_id: "my_team"
seed: 12345  # Your unique seed

simulation:
  population_size: 75000      # Adjust dataset size
  churn_base_rate: 0.055      # Higher churn
  promo_impact: 1.8           # Stronger promo effect
  # ... more parameters
```

### Run with Your Config

```bash
make all TEAM=configs/teams/my_team.yaml RUN_DATE=2026-02-01
```

## Run Tests

```bash
# Run all tests
make test

# Run specific test
pytest tests/test_generator_reproducible.py -v

# Check code quality
make lint
```

## Common Commands

```bash
# Clean generated data
make clean

# Show help
make help

# Run only data generation
make generate TEAM=configs/teams/team01.yaml RUN_DATE=2026-02-01

# Run only pipeline
make pipeline TEAM=configs/teams/team01.yaml RUN_DATE=2026-02-01
```

## Next Steps

1. **Explore the data**: Use notebooks to understand the Bronze/Silver/Gold layers
2. **Understand the models**: Check `src/md_lakehouse/models/` for implementation
3. **Read the docs**: See `docs/syllabus.md` for course structure
4. **Experiment**: Change team config parameters and see how results vary

## Troubleshooting

### Spark "Out of Memory"

Reduce dataset size in team config:

```yaml
simulation:
  population_size: 10000  # Smaller dataset
  months_history: 3       # Less history
```

### Import Errors

Ensure package is installed in editable mode:

```bash
pip install -e .
```

### Permission Errors (Windows)

Run PowerShell as Administrator or use WSL.

## Getting Help

- **Documentation**: Check `docs/` folder
- **Issues**: https://github.com/your-org/mineria-datos-lakehouse-template/issues
- **Discussions**: https://github.com/your-org/mineria-datos-lakehouse-template/discussions

---

**Ready to start?** Run `make all` and explore! 🚀
