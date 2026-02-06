[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/Dy4kZaBp)
# Minería de Datos - Lakehouse Template

[![CI](https://github.com/your-org/mineria-datos-lakehouse-template/actions/workflows/ci.yml/badge.svg)](https://github.com/your-org/mineria-datos-lakehouse-template/actions)

**Universidad Course Template** for teaching Data Mining and KDD using a modern local Lakehouse architecture.

## 🎯 Overview

This repository provides a **complete, production-ready template** for teaching Data Mining through hands-on projects. Students learn the full KDD (Knowledge Discovery in Databases) process while building a real-world analytics pipeline using industry-standard tools.

### Key Features

✅ **Local Lakehouse Architecture** (Bronze → Silver → Gold)  
✅ **PySpark ETL Pipelines** with data quality gates  
✅ **Snapshot Versioning** via `run_date` partitions (time-travel)  
✅ **Per-Team Data Simulation** with deterministic generators  
✅ **3 ML Models**: Churn Classification, LTV Regression, User Segmentation  
✅ **Comprehensive Testing** (reproducibility, quality, smoke tests)  
✅ **CI/CD Ready** with GitHub Actions  
✅ **Educational Notebooks** for guided learning

## 📚 Business Domain

**Digital Subscription Platform** (SaaS/Streaming/Learning App)

We simulate a realistic subscription business with:
- **Users** with demographics and acquisition channels
- **Subscriptions** (Basic, Standard, Premium plans)
- **Payments** (success/failure tracking)
- **Usage Logs** (sessions, minutes, feature usage)
- **Business Events** (promotions, outages, price changes)

### Analytics Use Cases

1. **Churn Prediction**: Identify users likely to cancel
2. **LTV Forecasting**: Predict customer lifetime value
3. **User Segmentation**: Group similar users for targeted strategies

## 🏗️ Architecture

### Lakehouse Layers

```
┌──────────────────────────────────────────────────────┐
│                    BRONZE LAYER                       │
│  Raw data (Parquet) - run_date partitioned          │
│  Tables: users, subscriptions, payments,             │
│          usage_logs, events                          │
└──────────────────────────────────────────────────────┘
                         ↓
┌──────────────────────────────────────────────────────┐
│                    SILVER LAYER                       │
│  Cleaned & validated data                            │
│  - Deduplication                                     │
│  - Range validation                                  │
│  - Referential integrity                             │
│  - Quality gates                                     │
└──────────────────────────────────────────────────────┘
                         ↓
┌──────────────────────────────────────────────────────┐
│                     GOLD LAYER                        │
│  Analytics & ML-ready features                       │
│  - fact_usage_daily                                  │
│  - fact_revenue_daily                                │
│  - churn_features & labels                           │
│  - customer_segments                                 │
│  - kpis_daily                                        │
└──────────────────────────────────────────────────────┘
                         ↓
┌──────────────────────────────────────────────────────┐
│                       MODELS                          │
│  Churn, LTV, Segmentation                            │
│  Metrics & Evaluation Reports                        │
└──────────────────────────────────────────────────────┘
```

### Time-Travel via Snapshots

Every table uses **partition folders** for versioning:

```
data/bronze/users/
├── run_date=2026-01-01/
├── run_date=2026-02-01/
└── run_date=2026-03-01/
```

Benefits:
- ✅ **Reproducibility**: Same seed + date = identical data
- ✅ **Auditability**: Full history of changes
- ✅ **Rollback**: Revert to previous snapshots
- ✅ **Comparison**: Analyze temporal evolution

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- 4GB RAM minimum (8GB recommended)
- Git

### Installation

```bash
# Clone repository
git clone https://github.com/your-org/mineria-datos-lakehouse-template.git
cd mineria-datos-lakehouse-template

# Install dependencies
make setup

# Or manually:
pip install -e ".[dev]"
```

### Run Complete Pipeline

```bash
# Run everything for team01
make all TEAM=configs/teams/team01.yaml RUN_DATE=2026-02-01

# Or step-by-step:
make generate TEAM=configs/teams/team01.yaml RUN_DATE=2026-02-01
make pipeline TEAM=configs/teams/team01.yaml RUN_DATE=2026-02-01
make features TEAM=configs/teams/team01.yaml RUN_DATE=2026-02-01
make train TEAM=configs/teams/team01.yaml RUN_DATE=2026-02-01
make evaluate TEAM=configs/teams/team01.yaml RUN_DATE=2026-02-01
```

### Using Python CLI Directly

```bash
# Generate Bronze data
python -m md_lakehouse.cli generate --team configs/teams/team01.yaml --run-date 2026-02-01

# Run ETL pipeline
python -m md_lakehouse.cli pipeline --team configs/teams/team01.yaml --run-date 2026-02-01

# Build ML features
python -m md_lakehouse.cli features --team configs/teams/team01.yaml --run-date 2026-02-01

# Train models
python -m md_lakehouse.cli train --team configs/teams/team01.yaml --run-date 2026-02-01

# Generate evaluation report
python -m md_lakehouse.cli evaluate --team configs/teams/team01.yaml --run-date 2026-02-01

# Run complete pipeline
python -m md_lakehouse.cli all --team configs/teams/team01.yaml --run-date 2026-02-01
```

## 📁 Project Structure

```
.
├── README.md
├── pyproject.toml                # Dependencies and project metadata
├── Makefile                      # Convenient CLI commands
├── configs/
│   ├── base.yaml                # Base configuration
│   └── teams/
│       ├── team01.yaml          # Team-specific configs (seed, params)
│       ├── team02.yaml
│       └── team03.yaml
├── data/                         # Generated data (git-ignored)
│   ├── bronze/                  # Raw data layer
│   ├── silver/                  # Cleaned data layer
│   ├── gold/                    # Analytics layer
│   ├── models/                  # Model metrics
│   └── reports/                 # Evaluation reports
├── src/md_lakehouse/
│   ├── cli.py                   # Command-line interface
│   ├── common/                  # Shared utilities
│   │   ├── spark.py            # Spark session management
│   │   ├── io.py               # I/O utilities
│   │   ├── config.py           # Config loading
│   │   └── hashing.py          # Reproducibility verification
│   ├── generator/               # Data generation
│   │   ├── generate.py
│   │   ├── schemas.py
│   │   └── logic.py
│   ├── pipelines/               # ETL pipelines
│   │   ├── bronze_to_silver.py
│   │   ├── silver_to_gold.py
│   │   └── quality.py
│   ├── features/
│   │   └── build_features.py
│   ├── models/
│   │   ├── churn.py
│   │   ├── ltv.py
│   │   └── segmentation.py
│   └── evaluation/
│       ├── metrics.py
│       └── reports.py
├── notebooks/                    # Educational Jupyter notebooks
│   ├── 00_intro.ipynb
│   ├── 01_kdd.ipynb
│   ├── 02_etl.ipynb
│   └── 03_models.ipynb
├── tests/                        # Comprehensive test suite
│   ├── test_generator_reproducible.py
│   ├── test_quality_rules.py
│   ├── test_gold_tables.py
│   └── test_models_smoke.py
├── docs/
│   ├── syllabus.md              # Course syllabus
│   ├── checkpoints.md           # Deliverables timeline
│   └── rubrica.md               # Grading rubric
└── .github/
    └── workflows/
        └── ci.yml               # GitHub Actions CI

## 🗂️ Estructura por Temas

Para facilitar el curso y las entregas, se añadieron carpetas por tema (al estilo del repo EDAII):

```
00-introduccion/     # Arranque y primer pipeline
01-kdd/              # Proceso KDD y relación con Lakehouse
02-bronze/           # Generación de datos crudos
03-silver/           # Limpieza y validación (quality gates)
04-gold/             # Tablas analíticas y KPIs
05-features/         # Ingeniería de características
06-modelos/          # Churn, LTV y Segmentación
07-evaluacion/       # Métricas y reportes
08-ci/               # Tests y GitHub Actions
09-proyecto/         # Proyecto final
entregas/
  ├─ tareas/         # PDFs por tarea (tarea_XX_apellido_nombre.pdf)
  └─ practicas/      # Código de prácticas con tests
ENTREGAS.md          # Guía de entregas (estructura y pasos)
```

Consulta el README dentro de cada carpeta de tema para objetivos, materiales y comandos.
```

## 🎓 Course Integration

### For Students

This template provides:
1. **Realistic data** generated deterministically per team
2. **Production patterns** (testing, CI/CD, documentation)
3. **Full KDD pipeline** from raw data to business insights
4. **Hands-on learning** with industry-standard tools

### For Instructors

Benefits:
- ✅ **Zero infrastructure setup** (runs locally)
- ✅ **Reproducible grading** (same seed = same results)
- ✅ **Configurable difficulty** via business parameters
- ✅ **Automated testing** for student submissions
- ✅ **Ready-to-use notebooks** for lectures

See [docs/syllabus.md](docs/syllabus.md) for detailed course structure.

## 🔧 Configuration System

### Team Configurations

Each team has a YAML config with:

```yaml
team_id: "team01"
seed: 42                          # For reproducibility

simulation:
  population_size: 60000          # Number of users
  months_history: 6               # Months to simulate
  churn_base_rate: 0.045          # 4.5% monthly churn
  price_sensitivity: 0.25
  promo_impact: 1.6               # 60% usage boost during promos
  outage_rate: 1.5                # Events per month
  outage_impact: 0.35             # Usage decrease
  payment_fail_base: 0.018
  seasonality_strength: 0.25
```

**Key principle**: Same `seed` + same `params` = **identical data** (guaranteed).

### Base Configuration

`configs/base.yaml` contains defaults that all teams inherit (with team overrides).

## ✅ Testing

Run the full test suite:

```bash
make test
```

Tests verify:
- ✅ **Reproducibility**: Same seed generates identical data
- ✅ **Quality Rules**: All data quality constraints pass
- ✅ **Gold Tables**: Correct schemas and data
- ✅ **Model Training**: Models train successfully and output metrics

### Reproducibility Example

```python
# Generate twice with same seed
generate_bronze_data(spark, config, team_id="test", seed=42, run_date="2026-02-01", output1)
generate_bronze_data(spark, config, team_id="test", seed=42, run_date="2026-02-01", output2)

# Verify identical
assert compute_dataframe_hash(df1) == compute_dataframe_hash(df2)  # ✓ PASS
```

## 📊 Expected Outputs

After running `make all`:

```
data/
├── bronze/
│   ├── users/run_date=2026-02-01/          (~50k-200k rows)
│   ├── subscriptions/run_date=2026-02-01/  (~50k-200k rows)
│   ├── payments/run_date=2026-02-01/       (~300k-1.2M rows)
│   ├── usage_logs/run_date=2026-02-01/     (~2M-10M rows)
│   └── events/run_date=2026-02-01/         (~20-50 rows)
├── silver/                                  (Same tables, cleaned)
├── gold/
│   ├── fact_usage_daily/
│   ├── fact_revenue_daily/
│   ├── churn_features/
│   ├── churn_labels/
│   ├── kpis_daily/
│   ├── ml_features/
│   └── customer_segments/
├── models/
│   ├── churn_metrics_2026-02-01.json
│   ├── ltv_metrics_2026-02-01.json
│   └── segmentation_metrics_2026-02-01.json
└── reports/
    └── evaluation_report_2026-02-01.md
```

### Sample Metrics

**Churn Model**:
- Accuracy: ~0.85-0.95
- F1 Score: ~0.60-0.80
- ROC AUC: ~0.75-0.90

**LTV Model**:
- R²: ~0.60-0.85
- MAE: ~$15-30

**Segmentation**:
- 4 clusters (VIP, Engaged, At-Risk, Inactive)
- Silhouette: ~0.40-0.60

## 🐛 Troubleshooting

### Issue: Spark "Out of Memory"

**Solution**: Reduce `population_size` in team config or increase memory:

```yaml
spark:
  memory: "4g"  # Increase from default 2g
```

### Issue: Tests fail with "FileNotFoundError"

**Solution**: Run `make generate` before tests, or use fixtures that generate data.

### Issue: CI takes too long

**Solution**: Enable CI mode in `configs/base.yaml`:

```yaml
ci_mode: true
ci_population: 2000
ci_months: 2
```

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure `make test` and `make lint` pass
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

## 📖 Citation

If you use this template in your course, please cite:

```bibtex
@software{mineria_datos_lakehouse,
  title={Minería de Datos - Local Lakehouse Template},
  author={Your Institution},
  year={2026},
  url={https://github.com/your-org/mineria-datos-lakehouse-template}
}
```

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/your-org/mineria-datos-lakehouse-template/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-org/mineria-datos-lakehouse-template/discussions)
- **Documentation**: See `docs/` folder

## 🌟 Acknowledgments

Built for teaching modern data engineering and machine learning practices using open-source tools.

---

**Happy Data Mining!** 🎓📊🚀
