# Changelog

All notable changes to FlexETL will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-02-07

### Added - Phase 1 MVP
- **Core ETL Pipeline**: End-to-end data processing
  - CSV extraction with error handling
  - Pandas-based transformations (filter, aggregate, calculate)
  - SQLite loading with verification
- **Container-Native**: OCI-compliant Docker image
  - Dockerfile with non-root user
  - docker-compose.yml for orchestration
  - Podman compatible
- **Data Processing**: E-commerce sales aggregation use case
  - Sample sales data (20 records)
  - Daily product revenue aggregation
  - Revenue calculation (quantity × unit_price)
- **Testing**: Comprehensive unit tests
  - pytest with >70% coverage
  - Tests for extractor, transformer, loader
  - fixtures and parametrized tests
- **Code Quality**: PEP 8 compliant
  - Type hints on all functions
  - Google-style docstrings
  - flake8, black, isort, mypy configs
- **Documentation**:
  - README.md with Docker/Podman quick start
  - CONTAINER.md compatibility guide
  - Inline code documentation
- **Configuration Files**:
  - requirements.txt and requirements-dev.txt
  - setup.cfg for linting/testing
  - .env.example template
  - .dockerignore for optimized builds

### Technical Details
- **Language**: Python 3.9+
- **Dependencies**: Pandas 2.0+
- **Base Image**: python:3.9-slim
- **Database**: SQLite3
- **Testing**: pytest, pytest-cov
- **Linting**: flake8, black, isort, mypy, bandit

### Deliverables
- Working ETL pipeline executable via `docker compose up pipeline`
- Sample data and expected outputs
- Unit tests with coverage reporting
- Container-first deployment

[0.1.0]: https://github.com/yourusername/FlexETL/releases/tag/v0.1.0
