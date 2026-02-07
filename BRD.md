# Business Requirements Document (BRD) for FlexETL Project

## Document Information
- **Document Title**: Business Requirements Document for FlexETL - Incremental ETL Framework
- **Version**: 2.0
- **Date**: February 07, 2026
- **Project Name**: FlexETL
- **Project Methodology**: Agile (Continuous Delivery with Independent Releases)
- **Previous Version**: 1.0 (Revised for MVP-first approach)

## Executive Summary
FlexETL v2.0 adopts a **working product first, then fix challenges incrementally** approach. Phase 1 delivers a minimal but complete ETL pipeline packaged as a container-native application. Each subsequent phase addresses ONE data engineering challenge and is independently deployable without breaking existing functionality. This ensures continuous value delivery and risk mitigation.

**Container-First Design**: Built with Docker as the primary deployment method while maintaining Podman compatibility, demonstrating modern DevOps practices and ensuring consistent execution across all environments.

## 1. Introduction

### 1.1 Purpose
This BRD defines requirements for FlexETL, a Python-based, container-native ETL framework built incrementally to address common data engineering challenges. The framework serves as:
- A **working reference implementation** for ETL patterns and containerization best practices
- A **portfolio project** showcasing software architecture and DevOps skills
- A **learning platform** for data engineering best practices

**Key Principles**:
- Ship working software early, enhance iteratively, maintain backward compatibility
- Container-first approach: Docker primary, Podman compatible
- Environment consistency: "Build once, run anywhere"

### 1.2 Document Scope
This BRD covers:
- Business objectives and success criteria
- Phased delivery with independent releases
- Functional requirements per phase
- Technical constraints and assumptions
- Risk management strategy

**Out of Scope**:
- Detailed technical design (covered in design docs per phase)
- Production cloud deployment (reference implementation only)
- Custom UI beyond CLI (may be added in future phases)

### 1.3 Revision History
- **v1.0**: Initial BRD with all challenges in early phases
- **v2.0**: Restructured to MVP-first with independent phases

### 1.4 References
- Agile Manifesto: Working software over comprehensive documentation
- Semantic Versioning for release management
- Twelve-Factor App principles for configuration

## 2. Project Vision

### 2.1 Background
Data engineering teams face recurring challenges: diverse sources, quality issues, scalability demands, and operational complexity. Most ETL frameworks are either too simple (scripts) or too complex (enterprise platforms). FlexETL bridges this gap by demonstrating production-ready patterns in an accessible, modular framework.

### 2.2 Business Objectives

**Primary Objective**: Build a working ETL pipeline that can be enhanced incrementally to solve data engineering challenges independently.

**Secondary Objectives**:
- Demonstrate software architecture best practices
- Create reusable patterns for future projects
- Showcase Python ecosystem capabilities
- Enable rapid prototyping for new ETL requirements
- Maintain production-ready code quality throughout

### 2.3 Success Criteria
- **Phase 1**: Working end-to-end ETL executable within 3 weeks
- **Overall**: Each phase independently deployable without regression
- **Quality**: >75% test coverage, PEP 8 compliant, documented
- **Usability**: New developer can run pipeline in <10 minutes

### 2.4 Target Audience
- **Primary**: Data engineers seeking reference implementations
- **Secondary**: Software architects evaluating ETL patterns
- **Tertiary**: Python developers learning data engineering

## 3. Data Engineering Challenges Addressed

FlexETL addresses these challenges progressively across phases:

1. **Basic ETL Operations** (Phase 1)
2. **Configuration Management** (Phase 2)
3. **Data Source Diversity** (Phase 3)
4. **Data Quality & Validation** (Phase 4)
5. **Fault Tolerance** (Phase 5)
6. **Orchestration & Scheduling** (Phase 6)
7. **Observability** (Phase 7)
8. **Scalability** (Phase 8)
9. **Multi-Target Loading** (Phase 9)
10. **Security & Compliance** (Phase 10)

## 4. Stakeholders

| Role | Name | Responsibility |
|------|------|----------------|
| Product Owner | Ajith | Prioritization, acceptance, roadmap |
| Developer | Ajith | Implementation, testing, documentation |
| End Users | Data Engineers | Adapt framework for specific use cases |
| Reviewers | Technical Community | Feedback and validation |

## 5. Use Case Definition

### 5.1 Primary Use Case: E-Commerce Sales Data Pipeline

**Business Scenario**: An e-commerce company needs daily sales reporting aggregated by product.

**Data Flow**:
```
CSV Files (sales_data.csv)
    → Extract
    → Transform (aggregate by product, calculate revenue)
    → Load (SQLite database)
```

**Input Schema**:
```csv
date,product_id,product_name,quantity,unit_price
2026-02-07,P001,Laptop,2,1200.00
2026-02-07,P002,Mouse,5,25.00
```

**Output Schema** (SQLite table: `daily_product_revenue`):
```sql
date DATE,
product_id TEXT,
product_name TEXT,
total_quantity INTEGER,
total_revenue DECIMAL
```

**Sample Transformation**:
- Group by date and product_id
- Sum quantity
- Calculate total_revenue = quantity * unit_price
- Remove records with null values

### 5.2 Success Metrics
- Pipeline completes in <5 seconds for 10K records
- 100% data accuracy (validated against manual calculation)
- Zero data loss
- Clear error messages on failure

## 6. Phased Release Plan

### Overview
Each phase is **independently releasable** and adds value without breaking prior functionality. Phases use semantic versioning (MAJOR.MINOR.PATCH).

---

## Phase 1: Working MVP (v0.1.0)
**Duration**: 2-3 weeks
**Goal**: End-to-end ETL that works

### Requirements
**FR1.1**: Extract data from CSV file
**FR1.2**: Transform data using Pandas (filter, aggregate)
**FR1.3**: Load data to SQLite database
**FR1.4**: Execute via containerized environment
**FR1.5**: Log execution status to console and file
**FR1.6**: Package application as OCI-compliant container image

**NFR1.1**: Complete execution in <10 seconds for 10K records
**NFR1.2**: Code follows PEP 8 standards
**NFR1.3**: Unit tests for each component (>70% coverage)
**NFR1.4**: Container build completes in <2 minutes
**NFR1.5**: Works with both Docker and Podman without modifications

### Technology Stack
- **Language**: Python 3.9+
- **Data Processing**: Pandas
- **Database**: SQLite3
- **Logging**: Python logging module
- **Testing**: pytest
- **Containerization**: Docker (primary) / Podman (compatible)
- **Base Image**: python:3.9-slim (official, OCI-compliant)

### Deliverables
- `flexetl/` - Source code package
  - `__init__.py`
  - `main.py` - Entry point
  - `extractor.py` - CSV extraction logic
  - `transformer.py` - Pandas transformation logic
  - `loader.py` - SQLite loading logic
- `tests/` - Unit tests
- `data/` - Sample input datasets
- `output/` - Pipeline outputs (gitignored)
- `Dockerfile` - OCI-compliant container image definition
- `docker-compose.yml` - Multi-container orchestration
- `.dockerignore` - Build optimization
- `requirements.txt` - Python dependencies
- `requirements-dev.txt` - Development dependencies
- `.env.example` - Environment variable template
- `README.md` - Container-first setup instructions
- `CONTAINER.md` - Docker/Podman compatibility guide

### Acceptance Criteria
- [ ] Run `docker compose up pipeline` successfully
- [ ] Run `podman-compose up pipeline` successfully (Podman test)
- [ ] Verify output in SQLite database matches expected results
- [ ] All tests pass via `docker compose run test`
- [ ] Container builds in <2 minutes
- [ ] Documentation includes Docker and Podman instructions
- [ ] Alternative local Python execution documented
- [ ] Volume mounts work for data input/output

### Dependencies
None (fresh start)

---

## Phase 2: Configuration-Driven Pipeline (v0.2.0)
**Duration**: 1-2 weeks
**Goal**: Remove hardcoded values, enable config-based execution

### Requirements
**FR2.1**: Read pipeline configuration from YAML file
**FR2.2**: Configure source file path, table name, transformations
**FR2.3**: Execute via `python main.py --config config.yaml`
**FR2.4**: Validate configuration schema on load

**NFR2.1**: Configuration changes require zero code changes
**NFR2.2**: Clear error messages for invalid config

### Technology Stack
- **New**: PyYAML, jsonschema (for config validation)
- **Retained**: All Phase 1 libraries

### Configuration Example
```yaml
version: "1.0"
pipeline:
  name: "sales_pipeline"
  source:
    type: "csv"
    path: "data/sales_data.csv"
  transformations:
    - type: "filter"
      column: "quantity"
      operator: ">"
      value: 0
    - type: "aggregate"
      group_by: ["date", "product_id"]
      aggregations:
        total_quantity: "sum(quantity)"
        total_revenue: "sum(quantity * unit_price)"
  target:
    type: "sqlite"
    database: "output.db"
    table: "daily_product_revenue"
```

### Deliverables
- `config_parser.py` - YAML parsing and validation
- `config.schema.json` - JSON schema for validation
- `sample_config.yaml` - Example configuration
- Updated `main.py` to accept --config argument
- Updated tests and documentation

### Acceptance Criteria
- [ ] Pipeline behavior changes via config without code edits
- [ ] Invalid config triggers clear error message
- [ ] All Phase 1 functionality still works
- [ ] Backward compatibility: Phase 1 code still runnable

### Dependencies
Phase 1 (v0.1.0) - Extends, not replaces

---

## Phase 3: Multi-Source Support (v0.3.0)
**Duration**: 1-2 weeks
**Goal**: Support multiple data source types via plugin architecture

### Requirements
**FR3.1**: Support CSV, JSON, and REST API sources
**FR3.2**: Plugin architecture for adding new sources
**FR3.3**: Source selection via configuration
**FR3.4**: Automatic schema detection where possible

**NFR3.1**: Adding new source type requires <100 lines of code
**NFR3.2**: Existing CSV functionality unchanged

### Technology Stack
- **New**: requests (for REST API)
- **Retained**: All previous libraries

### Source Plugin Interface
```python
class BaseSource(ABC):
    @abstractmethod
    def extract(self, config: dict) -> pd.DataFrame:
        pass
```

### Configuration Example
```yaml
source:
  type: "api"  # or "csv" or "json"
  url: "https://api.example.com/sales"
  auth:
    type: "bearer"
    token_env: "API_TOKEN"
  params:
    start_date: "2026-02-01"
    end_date: "2026-02-07"
```

### Deliverables
- `sources/` package with base class and implementations
  - `base_source.py`
  - `csv_source.py`
  - `json_source.py`
  - `api_source.py`
- `source_factory.py` - Factory pattern for source selection
- Updated configuration schema
- Tests for each source type
- Documentation for adding custom sources

### Acceptance Criteria
- [ ] Successfully extract from CSV, JSON, and API
- [ ] Switch sources via config without code changes
- [ ] Phase 1 and 2 pipelines still work
- [ ] Documentation shows how to add custom source

### Dependencies
Phase 2 (v0.2.0) - Extends configuration

---

## Phase 4: Data Quality & Validation (v0.4.0)
**Duration**: 1-2 weeks
**Goal**: Validate data quality and detect issues early

### Requirements
**FR4.1**: Schema validation for input data
**FR4.2**: Data quality checks (nulls, duplicates, ranges)
**FR4.3**: Configurable validation rules
**FR4.4**: Validation report generation
**FR4.5**: Pipeline behavior on validation failure (fail/warn/continue)

**NFR4.1**: Validation adds <10% overhead to execution time
**NFR4.2**: Clear, actionable error messages

### Technology Stack
- **New**: Pandera (data validation)
- **Retained**: All previous libraries

### Validation Configuration
```yaml
validation:
  schema:
    date:
      type: "date"
      nullable: false
    quantity:
      type: "integer"
      min: 0
      max: 10000
    unit_price:
      type: "float"
      min: 0.01
  quality_checks:
    - type: "no_duplicates"
      columns: ["date", "product_id"]
    - type: "null_check"
      columns: ["product_id", "quantity"]
      max_null_percentage: 0
  on_failure: "fail"  # or "warn" or "continue"
```

### Deliverables
- `validators/` package
  - `schema_validator.py`
  - `quality_checker.py`
  - `validation_reporter.py`
- Integration with pipeline execution
- Validation report output (JSON/HTML)
- Tests for validation logic
- Documentation on validation rules

### Acceptance Criteria
- [ ] Invalid data triggers validation errors
- [ ] Validation report shows issues clearly
- [ ] Pipeline behavior configurable on failure
- [ ] Previous phases work with validation disabled

### Dependencies
Phase 2 (v0.2.0) - Extends configuration

---

## Phase 5: Fault Tolerance & Retry Logic (v0.5.0)
**Duration**: 1-2 weeks
**Goal**: Handle transient failures gracefully

### Requirements
**FR5.1**: Retry logic for failed operations (configurable attempts)
**FR5.2**: Exponential backoff between retries
**FR5.3**: Dead letter queue for permanently failed records
**FR5.4**: Checkpoint mechanism for resuming failed pipelines
**FR5.5**: Detailed error logging with stack traces

**NFR5.1**: Transient network failures don't fail pipeline
**NFR5.2**: Failed records isolated, don't block entire batch

### Technology Stack
- **New**: tenacity (retry library)
- **Retained**: All previous libraries

### Retry Configuration
```yaml
fault_tolerance:
  retry:
    enabled: true
    max_attempts: 3
    backoff_strategy: "exponential"
    backoff_multiplier: 2
    max_backoff_seconds: 60
  dead_letter_queue:
    enabled: true
    path: "failed_records/"
  checkpoints:
    enabled: true
    interval: 1000  # records
```

### Deliverables
- `fault_tolerance/` package
  - `retry_handler.py`
  - `dead_letter_queue.py`
  - `checkpoint_manager.py`
- Integration with extract/transform/load operations
- Failed records tracking and reporting
- Tests for retry scenarios
- Documentation on recovery procedures

### Acceptance Criteria
- [ ] Simulated transient failure auto-recovers
- [ ] Permanent failures logged to DLQ
- [ ] Pipeline resumes from checkpoint after interruption
- [ ] Previous phases work with fault tolerance disabled

### Dependencies
Phase 1 (v0.1.0) - Wraps execution logic

---

## Phase 6: Orchestration & Scheduling (v0.6.0)
**Duration**: 2 weeks
**Goal**: Automate pipeline execution on schedule

### Requirements
**FR6.1**: Schedule pipelines via cron-like expressions
**FR6.2**: Execute multiple pipelines in sequence or parallel
**FR6.3**: Execution history tracking
**FR6.4**: Manual trigger capability
**FR6.5**: Execution status API (running/success/failed)

**NFR6.1**: Scheduler runs as daemon process
**NFR6.2**: Graceful shutdown without data loss

### Technology Stack
- **New**: Celery + Redis (task queue) OR APScheduler (lighter option)
- **Retained**: All previous libraries

### Schedule Configuration
```yaml
scheduler:
  pipelines:
    - name: "daily_sales"
      config: "configs/sales_pipeline.yaml"
      schedule: "0 2 * * *"  # Daily at 2 AM
      enabled: true
    - name: "hourly_inventory"
      config: "configs/inventory_pipeline.yaml"
      schedule: "0 * * * *"  # Hourly
      enabled: false
  execution_history:
    retention_days: 30
    storage: "sqlite"
```

### Deliverables
- `scheduler/` package
  - `task_scheduler.py`
  - `execution_tracker.py`
  - `api_server.py` (Flask-based status API)
- CLI for scheduler management (`flexetl scheduler start/stop/status`)
- Execution history database
- Tests for scheduling logic
- Documentation on scheduler setup

### Acceptance Criteria
- [ ] Pipeline executes on schedule
- [ ] Execution history queryable
- [ ] Manual trigger works via CLI
- [ ] Can run pipelines without scheduler (Phase 1 still works)

### Dependencies
Phase 2 (v0.2.0) - Uses configuration

---

## Phase 7: Monitoring & Observability (v0.7.0)
**Duration**: 1-2 weeks
**Goal**: Visibility into pipeline performance and health

### Requirements
**FR7.1**: Collect metrics (records processed, duration, errors)
**FR7.2**: Health check endpoint
**FR7.3**: Performance metrics export (Prometheus format)
**FR7.4**: Log aggregation and searchability
**FR7.5**: Alert on failure thresholds

**NFR7.1**: Metrics collection adds <5% overhead
**NFR7.2**: Metrics retained for 30 days

### Technology Stack
- **New**: prometheus_client, structlog
- **Retained**: All previous libraries

### Metrics Configuration
```yaml
monitoring:
  metrics:
    enabled: true
    port: 9090
    path: "/metrics"
  logging:
    level: "INFO"
    format: "json"
    output: "logs/flexetl.log"
    rotation: "daily"
  alerts:
    - type: "failure_rate"
      threshold: 0.1  # 10%
      window: "1h"
      action: "log"  # or "email" in future
```

### Metrics Tracked
- Pipeline execution count (success/failure)
- Records processed per pipeline
- Execution duration (p50, p95, p99)
- Error rate by error type
- Data quality check failures

### Deliverables
- `monitoring/` package
  - `metrics_collector.py`
  - `health_checker.py`
  - `alert_manager.py`
- Prometheus metrics endpoint
- Grafana dashboard template (JSON)
- Structured logging integration
- Tests for metrics collection
- Documentation on monitoring setup

### Acceptance Criteria
- [ ] Metrics accessible via HTTP endpoint
- [ ] Grafana dashboard displays pipeline metrics
- [ ] Health check returns pipeline status
- [ ] Can disable monitoring (previous phases work)

### Dependencies
Phase 1 (v0.1.0) - Instruments execution

---

## Phase 8: Scalability - Large Dataset Handling (v0.8.0)
**Duration**: 2-3 weeks
**Goal**: Process datasets that don't fit in memory

### Requirements
**FR8.1**: Chunked processing for large files
**FR8.2**: Parallel processing of independent chunks
**FR8.3**: Memory-efficient transformations
**FR8.4**: Progress tracking for long-running jobs

**NFR8.1**: Process 10GB file with <2GB memory usage
**NFR8.2**: Near-linear speedup with CPU cores

### Technology Stack
- **New**: Dask (parallel processing)
- **Retained**: All previous libraries

### Scalability Configuration
```yaml
scalability:
  processing:
    mode: "chunked"  # or "dask" or "standard"
    chunk_size: 100000  # records
    parallel_workers: 4
  memory:
    limit_mb: 2048
    spill_to_disk: true
```

### Deliverables
- `scalability/` package
  - `chunked_processor.py`
  - `dask_processor.py`
  - `memory_manager.py`
- Refactored transformers to support streaming
- Progress bar for long operations
- Performance benchmarks
- Tests with large datasets
- Documentation on performance tuning

### Acceptance Criteria
- [ ] Process 1GB file successfully
- [ ] Memory usage stays under configured limit
- [ ] Progress visible during execution
- [ ] Small datasets still use standard mode (no overhead)

### Dependencies
Phase 1 (v0.1.0) - Alternative execution engine

---

## Phase 9: Multi-Target Loading (v0.9.0)
**Duration**: 1 week
**Goal**: Load to multiple destinations simultaneously

### Requirements
**FR9.1**: Support multiple target types (PostgreSQL, Parquet, CSV)
**FR9.2**: Plugin architecture for targets
**FR9.3**: Load to multiple targets in one pipeline run
**FR9.4**: Target-specific optimizations (batch inserts, partitioning)

**NFR9.1**: Adding new target type requires <100 lines of code
**NFR9.2**: Multi-target adds <20% overhead vs single target

### Technology Stack
- **New**: psycopg2 (PostgreSQL), pyarrow (Parquet)
- **Retained**: All previous libraries

### Target Configuration
```yaml
targets:
  - type: "sqlite"
    database: "output.db"
    table: "daily_revenue"
    mode: "replace"
  - type: "postgresql"
    connection_string_env: "POSTGRES_URL"
    table: "daily_revenue"
    schema: "analytics"
    mode: "append"
  - type: "parquet"
    path: "output/daily_revenue.parquet"
    partition_by: ["date"]
```

### Deliverables
- `targets/` package (mirror of sources)
  - `base_target.py`
  - `sqlite_target.py`
  - `postgresql_target.py`
  - `parquet_target.py`
- `target_factory.py`
- Parallel loading support
- Tests for each target type
- Documentation for adding custom targets

### Acceptance Criteria
- [ ] Successfully load to SQLite, PostgreSQL, and Parquet
- [ ] Multiple targets loaded in one run
- [ ] Phase 1 SQLite-only mode still works
- [ ] Documentation shows custom target creation

### Dependencies
Phase 3 (v0.3.0) - Mirrors source plugin architecture

---

## Phase 10: Security & Compliance (v1.0.0)
**Duration**: 1-2 weeks
**Goal**: Secure credential management and basic compliance

### Requirements
**FR10.1**: Load credentials from environment variables
**FR10.2**: Encrypt sensitive configuration values
**FR10.3**: Audit logging for data access
**FR10.4**: PII detection and masking (basic patterns)
**FR10.5**: Secure file permissions on outputs

**NFR10.1**: No credentials in code or plain-text config
**NFR10.2**: Audit logs tamper-evident

### Technology Stack
- **New**: cryptography (encryption), python-dotenv
- **Retained**: All previous libraries

### Security Configuration
```yaml
security:
  credentials:
    source: "environment"  # or "encrypted_file"
  encryption:
    enabled: true
    key_env: "FLEXETL_ENCRYPTION_KEY"
  audit:
    enabled: true
    log_path: "audit/audit.log"
    events: ["data_access", "config_change", "execution"]
  pii_masking:
    enabled: true
    fields: ["email", "phone", "ssn"]
    strategy: "hash"  # or "redact"
```

### Deliverables
- `security/` package
  - `credential_manager.py`
  - `encryption_handler.py`
  - `audit_logger.py`
  - `pii_detector.py`
- `.env.example` template
- Encrypted config file support
- Security documentation and best practices
- Security tests
- Compliance checklist

### Acceptance Criteria
- [ ] No credentials in config files
- [ ] Encrypted config values decryptable at runtime
- [ ] Audit log tracks all data access
- [ ] PII fields masked in logs and outputs
- [ ] Security scan passes (bandit, safety)

### Dependencies
Phase 2 (v0.2.0) - Secures configuration

---

## 7. Technical Architecture Principles

### 7.1 Design Principles
- **SOLID**: Single responsibility, Open/closed, Liskov substitution, Interface segregation, Dependency inversion
- **DRY**: Don't repeat yourself - reusable components
- **KISS**: Keep it simple - avoid over-engineering
- **YAGNI**: You aren't gonna need it - build for current needs

### 7.2 Code Quality Standards
- **PEP 8**: Python code style compliance (max line length 79)
- **Type Hints**: All functions have type annotations
- **Docstrings**: Google-style docstrings for all public APIs
- **Test Coverage**: Minimum 75% coverage per phase
- **Security**: No hardcoded credentials, input validation, secure defaults

### 7.3 Module Structure
```
flexetl/
├── core/
│   ├── pipeline.py          # Core pipeline orchestration
│   ├── config.py            # Configuration management
│   └── exceptions.py        # Custom exceptions
├── sources/                 # Data source plugins
├── transformers/            # Transformation logic
├── targets/                 # Data target plugins
├── validators/              # Data validation
├── monitoring/              # Observability
├── scheduler/               # Orchestration
├── security/                # Security features
└── utils/                   # Shared utilities

tests/                       # Mirror of source structure
docs/                        # Documentation
configs/                     # Sample configurations
data/                        # Sample datasets
```

### 7.4 Backward Compatibility
- **Semantic Versioning**: MAJOR.MINOR.PATCH
- **Deprecation Policy**: 2 minor versions notice before removal
- **Configuration Versions**: Support previous config schema
- **API Stability**: Public APIs stable within major version

## 8. Non-Functional Requirements (Cross-Phase)

### 8.1 Performance
- **Response Time**: Pipeline startup <2 seconds
- **Throughput**: Process 10K records/second (small records)
- **Memory**: <500MB for datasets <1GB (Phase 1-7)
- **Concurrency**: Support 10+ concurrent pipelines (Phase 6+)

### 8.2 Reliability
- **Availability**: Framework code has no single points of failure
- **Data Integrity**: Zero data loss under normal operation
- **Error Recovery**: Automatic retry for transient failures (Phase 5+)
- **Testing**: All features have automated tests

### 8.3 Usability
- **Setup Time**: <10 minutes from clone to first run
- **Documentation**: README, API docs, tutorials, examples
- **Error Messages**: Clear, actionable, include context
- **CLI**: Intuitive commands with help text

### 8.4 Maintainability
- **Code Organization**: Modular, loosely coupled
- **Dependencies**: Minimal, well-maintained libraries
- **Logging**: Comprehensive, structured logs
- **Monitoring**: Observable metrics (Phase 7+)

### 8.5 Security
- **Credentials**: Environment variables or encrypted config
- **Dependencies**: Regular security scans (safety, bandit)
- **Input Validation**: All external data validated
- **Least Privilege**: Minimal file system permissions

### 8.6 Portability
- **Container Runtime**: Docker (primary), Podman (compatible), any OCI-compliant runtime
- **OS Support**: Linux, macOS, Windows (via container runtime)
- **Python Versions**: 3.9+ (managed via container base image)
- **Database**: SQLite (Phase 1), containerized PostgreSQL (Phase 9+)
- **Deployment**: Container-native (Docker Compose, Podman Compose)
- **Alternative**: Local Python execution supported but not primary method

## 9. Development Standards

### 9.1 Version Control
- **Branching**: main (stable), develop (integration), feature/* (work)
- **Commits**: Conventional commits format (feat:, fix:, docs:, etc.)
- **Pull Requests**: Required for all changes, reviewed before merge
- **Tagging**: Git tags for all releases (v0.1.0, v0.2.0, etc.)

### 9.2 Testing Strategy
- **Unit Tests**: pytest, >75% coverage per module
- **Integration Tests**: End-to-end pipeline tests
- **Performance Tests**: Benchmark critical paths (Phase 8)
- **Security Tests**: bandit (static), safety (dependencies)

### 9.3 Documentation Requirements
- **README.md**: Quick start, installation, basic usage
- **API Documentation**: Auto-generated from docstrings (Sphinx)
- **Tutorials**: Step-by-step guides for common scenarios
- **Architecture Docs**: Design decisions, patterns used
- **Changelog**: Keep updated per release

### 9.4 CI/CD Pipeline
- **Linting**: flake8, black, isort
- **Type Checking**: mypy
- **Testing**: Automated test runs on PRs (containerized)
- **Container Build**: Automated image builds on commits
- **Multi-Runtime Testing**: Test on both Docker and Podman
- **Security**: Container and dependency scans (trivy, bandit, safety)
- **Release**: Automated tagging, changelog, and container image publishing

### 9.5 Containerization Standards
- **OCI Compliance**: Images follow Open Container Initiative standards
- **Base Image**: Official python:3.9-slim (regularly updated)
- **Multi-Stage Builds**: Separate build and runtime stages (Phase 2+)
- **Image Size**: Optimize for minimal size (<200MB for Phase 1)
- **Security**:
  - Non-root user for container execution
  - No secrets in image layers
  - Minimal packages (only runtime dependencies)
  - Regular base image updates
- **Tagging Strategy**:
  - `latest` - most recent release
  - `v0.1.0` - semantic version tags
  - `dev` - development branch
- **Layer Optimization**:
  - Dependencies before source code
  - Proper use of `.dockerignore`
  - Combined RUN commands where appropriate
- **Podman Compatibility**:
  - No Docker-specific features (BuildKit only if compatible)
  - Volume mounts use relative paths
  - Network configuration portable
  - Test with `podman-compose` in CI
- **Environment Variables**:
  - All configuration via ENV vars
  - `.env` file support for local development
  - No hardcoded values in Dockerfile
- **Health Checks**: Container health endpoints (Phase 6+)
- **Labels**: OCI annotations for metadata (version, source, etc.)

## 10. Risk Management

### 10.1 Technical Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Library compatibility issues | Medium | Medium | Pin dependencies, test across Python versions |
| Performance bottlenecks | Medium | High | Early benchmarking (Phase 8), optimize critical paths |
| API design mistakes | High | High | Start simple, gather feedback, deprecate carefully |
| Security vulnerabilities | Low | Critical | Regular scans, follow best practices, security reviews |
| Scope creep per phase | Medium | Medium | Strict phase boundaries, backlog management |

### 10.2 Project Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Time estimates too optimistic | Medium | Medium | Buffer in timelines, MVP-first approach |
| Dependency on external tools | Low | Medium | Minimize external dependencies, document alternatives |
| Lack of user feedback | Medium | High | Early releases, community engagement |
| Technical debt accumulation | Medium | High | Regular refactoring, code reviews, technical debt sprints |

### 10.3 Mitigation Strategies
- **Incremental Delivery**: Each phase adds value independently
- **Automated Testing**: Catch regressions early
- **Documentation**: Maintain as code evolves
- **Community**: Seek feedback from Phase 1 onwards
- **Flexibility**: Adjust roadmap based on learnings

## 11. Assumptions and Constraints

### 11.1 Assumptions
- Docker or Podman installed in development environment
- Container runtime supports OCI-compliant images
- SQLite sufficient for initial data storage
- Users comfortable with CLI and container commands
- Sample datasets available for testing
- Internet access for downloading dependencies and base images

### 11.2 Constraints
- **Language**: Python (core requirement)
- **Licensing**: Open source (MIT or Apache 2.0)
- **Resources**: Single developer (Ajith)
- **Timeline**: Flexible but prefer 3-4 months for v1.0
- **Infrastructure**: Local development, no cloud costs

### 11.3 Dependencies
- **Container Runtime**: Docker 20.10+ or Podman 3.0+
- **Compose Tool**: docker-compose 2.0+ or podman-compose 1.0+
- **Third-Party Libraries**: Available via PyPI
- **Development Tools**: Git, IDE (VSCode/PyCharm)
- **Testing**: pytest framework (containerized)
- **Documentation**: Markdown, Sphinx
- **Optional**: Local Python 3.9+ for non-containerized development

## 12. Success Metrics

### 12.1 Phase Completion Metrics
- **Functionality**: All FRs implemented and tested
- **Quality**: Tests pass, coverage >75%, linting clean
- **Documentation**: README updated, examples provided
- **Release**: Tagged, changelog updated, deployable

### 12.2 Overall Project Metrics
- **Code Quality**: Zero critical flake8/bandit issues
- **Test Coverage**: >80% by v1.0
- **Performance**: Meets NFRs per phase
- **Usability**: Can run pipeline within 10 minutes
- **Adoption**: GitHub stars, forks, usage examples

### 12.3 Learning Objectives
- Demonstrate ETL architecture patterns
- Showcase Python best practices
- Master containerization and DevOps practices
- Build portfolio-worthy project with modern deployment
- Master data engineering concepts
- Practice agile delivery
- Showcase Docker/Podman compatibility expertise

## 13. Acceptance Criteria (Overall)

### 13.1 Phase 1 (MVP) Acceptance
- [ ] Extract CSV data successfully
- [ ] Transform data with Pandas
- [ ] Load data to SQLite
- [ ] Execute via `docker compose up pipeline`
- [ ] Execute via `podman-compose up pipeline` (Podman compatibility test)
- [ ] Tests pass with >70% coverage (containerized)
- [ ] Container builds in <2 minutes
- [ ] Documentation covers Docker and Podman setup
- [ ] PEP 8 compliant
- [ ] OCI-compliant container image

### 13.2 v1.0 (Phase 10) Acceptance
- [ ] All 10 phases completed
- [ ] Each phase independently functional
- [ ] No regressions from previous phases
- [ ] Test coverage >80%
- [ ] Comprehensive documentation
- [ ] Security scan passes
- [ ] Performance benchmarks met
- [ ] Can adapt to new use case within 1 hour

### 13.3 Quality Gates
- **Code Reviews**: All PRs reviewed before merge
- **Automated Tests**: CI passes required for merge
- **Security Scans**: No critical/high vulnerabilities
- **Documentation**: Updated with each phase
- **Demo**: Working demo for each phase release

## 14. Glossary

- **ETL**: Extract, Transform, Load - data integration pattern
- **MVP**: Minimum Viable Product - simplest working version
- **OCI**: Open Container Initiative - container image standards
- **Docker**: Container platform and runtime
- **Podman**: Daemonless container engine, OCI-compliant
- **DLQ**: Dead Letter Queue - storage for failed records
- **PII**: Personally Identifiable Information
- **CI/CD**: Continuous Integration/Continuous Deployment
- **NFR**: Non-Functional Requirement
- **FR**: Functional Requirement

## 15. Appendices

### Appendix A: Sample Commands

#### Docker Commands (Primary)
```bash
# Phase 1: Build and run pipeline
docker compose build
docker compose up pipeline

# Run tests
docker compose run test

# Phase 2: Config-driven execution
docker compose run pipeline --config configs/sales_pipeline.yaml

# Development mode (with volume mounts)
docker compose up --build

# Phase 6: Scheduler
docker compose up scheduler
docker compose exec scheduler flexetl status

# Phase 7: Health checks and metrics
curl http://localhost:9090/health
curl http://localhost:9090/metrics

# Cleanup
docker compose down
docker compose down -v  # Remove volumes
```

#### Podman Commands (Compatible)
```bash
# Phase 1: Build and run pipeline
podman-compose build
podman-compose up pipeline

# Run tests
podman-compose run test

# Phase 2: Config-driven execution
podman-compose run pipeline --config configs/sales_pipeline.yaml

# Alternative: Using podman directly
podman build -t flexetl:latest .
podman run -v ./data:/app/data:ro -v ./output:/app/output flexetl:latest

# Cleanup
podman-compose down
```

#### Local Python (Alternative)
```bash
# Setup
python -m venv venv
source venv/bin/activate  # Linux/macOS
# OR: venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Phase 1: Basic execution
python -m flexetl.main

# Phase 2: Config-driven
python -m flexetl.main --config configs/sales_pipeline.yaml

# Run tests
pytest tests/ -v --cov=flexetl
```

### Appendix B: Technology Evaluation

| Phase | Technology | Alternative Considered | Decision Rationale |
|-------|-----------|------------------------|-------------------|
| 1 | Docker | Kubernetes | Docker simpler, K8s overkill for Phase 1 |
| 1 | Podman Compatible | Docker Only | Podman shows broader containerization knowledge |
| 1 | Pandas | Polars | Pandas more mature, widely known |
| 1 | SQLite | PostgreSQL | SQLite no setup, sufficient for Phase 1 |
| 4 | Pandera | Great Expectations | Pandera lighter, Pandas-native |
| 6 | APScheduler | Celery | APScheduler simpler for single-machine |
| 8 | Dask | PySpark | Dask more Pandas-like, easier learning curve |

### Appendix C: Release Checklist Template
- [ ] All FRs implemented
- [ ] Tests written and passing (containerized)
- [ ] Documentation updated (Docker and Podman)
- [ ] CHANGELOG.md updated
- [ ] Version bumped in setup.py and Dockerfile
- [ ] Container image builds successfully
- [ ] Docker compatibility verified
- [ ] Podman compatibility verified
- [ ] Container security scan passed (trivy)
- [ ] Image size optimized (<200MB Phase 1)
- [ ] Git tag created
- [ ] Container image tagged and pushed
- [ ] Demo prepared (containerized)
- [ ] Backward compatibility verified
- [ ] Performance benchmarks run
- [ ] Dependency security scan passed (safety, bandit)

## 16. Change Log

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-07 | Ajith | Initial BRD with all challenges in early phases |
| 2.0 | 2026-02-07 | Ajith | Restructured to MVP-first, independent phases, detailed requirements |
| 2.1 | 2026-02-07 | Ajith | Updated to container-first approach with Docker primary, Podman compatible |

## 17. Approval

**Document Status**: Ready for Development

**Product Owner Approval**: _____________________  Date: ___________

**Technical Review**: _____________________  Date: ___________

---

## Next Steps

1. **Review BRD v2.0**: Validate approach and phase breakdown
2. **Setup Development Environment**: Python, Git, IDE
3. **Create Project Structure**: Initialize repository, folders
4. **Begin Phase 1 Development**: Build working MVP
5. **Iterate**: Deliver phases incrementally, gather feedback

**Note**: This BRD is a living document. As each phase completes and we learn, refinements to future phases are expected and encouraged. The goal is working software and continuous improvement.
