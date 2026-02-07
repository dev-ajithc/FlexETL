# FlexETL

**Container-Native ETL Framework for Data Engineering**

[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](https://github.com/yourusername/FlexETL)
[![Python](https://img.shields.io/badge/python-3.9+-green.svg)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/docker-compatible-blue.svg)](https://www.docker.com/)
[![Podman](https://img.shields.io/badge/podman-compatible-purple.svg)](https://podman.io/)

FlexETL is a modular, container-native ETL (Extract, Transform, Load) framework built incrementally to address common data engineering challenges. This Phase 1 MVP demonstrates a working end-to-end pipeline that extracts sales data from CSV, transforms it using Pandas, and loads it into SQLite.

## 🎯 Project Goals

- **Working Reference Implementation**: Showcase ETL patterns and containerization best practices
- **Portfolio Project**: Demonstrate software architecture and DevOps skills
- **Learning Platform**: Educational resource for data engineering concepts
- **Agile Delivery**: Build incrementally, ship independently releasable phases

## 🚀 Quick Start (Docker)

### Prerequisites

FlexETL requires a container runtime. Choose Docker (recommended for beginners) or Podman (better security).

#### Option 1: Docker Installation

**Linux (Ubuntu/Debian):**
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
newgrp docker

# Verify installation
docker --version
docker compose version
```

**Linux (Fedora/RHEL/CentOS):**
```bash
sudo dnf install docker docker-compose-plugin
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER
newgrp docker
```

**macOS:**
```bash
# Using Homebrew
brew install --cask docker

# Or download Docker Desktop from:
# https://www.docker.com/products/docker-desktop
```

**Windows:**
- Download Docker Desktop from [docker.com](https://www.docker.com/products/docker-desktop)
- Follow installation wizard
- Enable WSL 2 backend when prompted

#### Option 2: Podman Installation

**Linux (Fedora/RHEL/CentOS):**
```bash
sudo dnf install podman podman-compose
podman --version
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install podman podman-compose
podman --version
```

**macOS:**
```bash
brew install podman podman-compose

# Initialize Podman machine
podman machine init
podman machine start
podman machine list
```

**Windows:**
- Download from [podman.io](https://podman.io/getting-started/installation#windows)
- Follow installation wizard

#### Verify Installation

```bash
# For Docker
docker --version
docker compose version

# For Podman
podman --version
podman-compose --version
```

### Run the Pipeline

```bash
# Clone the repository
git clone <repository-url>
cd FlexETL

# Build and run
docker compose up pipeline

# View results
sqlite3 output/sales.db "SELECT * FROM daily_product_revenue;"
```

That's it! The pipeline will extract, transform, and load the sample sales data.

## 📦 What's in Phase 1 (v0.1.0)

### Features
- ✅ Extract data from CSV files
- ✅ Transform data with Pandas (filter, aggregate, calculate)
- ✅ Load data to SQLite database
- ✅ Containerized execution (Docker/Podman compatible)
- ✅ Comprehensive logging
- ✅ Unit tests with >70% coverage
- ✅ PEP 8 compliant code

### Use Case: E-Commerce Sales Aggregation
The pipeline processes daily sales data and aggregates it by product:

**Input**: `data/sales_data.csv`
```csv
date,product_id,product_name,quantity,unit_price
2026-02-01,P001,Laptop,2,1200.00
2026-02-01,P002,Mouse,5,25.00
...
```

**Output**: `output/sales.db` → `daily_product_revenue` table
```
date | product_id | product_name | total_quantity | total_revenue
```

## 🐳 Docker Usage (Recommended)

### Build Image
```bash
docker compose build
```

### Run Pipeline
```bash
docker compose up pipeline
```

### Run Tests
```bash
docker compose run test
```

### Development Mode (Hot Reload)
```bash
# Mount source code for live changes
docker compose up --build
```

### Cleanup
```bash
docker compose down
docker compose down -v  # Remove volumes
```

## 🦭 Podman Usage (Alternative)

FlexETL is fully compatible with Podman. Use these commands if you have Docker restrictions or prefer rootless containers.

### Using podman-compose (Recommended)

```bash
# Build image
podman-compose build

# Run pipeline
podman-compose up pipeline

# Run tests
podman-compose run test

# Development mode (hot reload)
podman-compose up --build

# Run in background
podman-compose up -d pipeline

# View logs
podman-compose logs -f pipeline

# Stop and cleanup
podman-compose down
podman-compose down -v  # Remove volumes
```

### Using podman directly (Without compose)

```bash
# Build image
podman build -t flexetl:latest .

# Run pipeline
podman run --rm \
  -v ./data:/app/data:ro \
  -v ./output:/app/output \
  -e LOG_LEVEL=INFO \
  flexetl:latest

# Run tests
podman run --rm \
  -v ./flexetl:/app/flexetl \
  -v ./tests:/app/tests \
  -v ./requirements-dev.txt:/app/requirements-dev.txt \
  flexetl:latest \
  sh -c "pip install -r requirements-dev.txt && pytest tests/ -v"

# Interactive shell for debugging
podman run -it --rm \
  -v ./flexetl:/app/flexetl \
  -v ./data:/app/data:ro \
  -v ./output:/app/output \
  flexetl:latest \
  /bin/bash

# View logs (for background containers)
podman ps  # Get container ID
podman logs -f <container-id>

# Stop and remove containers
podman stop <container-id>
podman rm <container-id>

# List and remove images
podman images
podman rmi flexetl:latest
```

### Podman Machine Setup (macOS/Windows)

If Podman machine is not running:

```bash
# Check machine status
podman machine list

# Start machine
podman machine start

# Verify
podman --version
podman machine ssh  # Test connection
```

### View Results

```bash
# After pipeline runs, view output
sqlite3 output/sales.db "SELECT * FROM daily_product_revenue;"

# Or enter SQLite interactive mode
sqlite3 output/sales.db
sqlite> .tables
sqlite> .schema daily_product_revenue
sqlite> SELECT * FROM daily_product_revenue LIMIT 5;
sqlite> .quit
```

**Note**: Podman commands are identical to Docker - just replace `docker` with `podman` and `docker-compose` with `podman-compose`!

See [CONTAINER.md](CONTAINER.md) for detailed Docker/Podman compatibility guide and troubleshooting.

## 🐍 Local Python (Alternative)

If you prefer non-containerized development:

```bash
# Setup virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# OR: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run pipeline
python -m flexetl.main

# Run tests
pip install -r requirements-dev.txt
pytest tests/ -v --cov=flexetl
```

## 📁 Project Structure

```
FlexETL/
├── flexetl/               # Source code package
│   ├── __init__.py
│   ├── main.py           # Pipeline entry point
│   ├── extractor.py      # CSV extraction
│   ├── transformer.py    # Data transformations
│   └── loader.py         # SQLite loading
├── tests/                 # Unit tests
│   ├── test_extractor.py
│   ├── test_transformer.py
│   └── test_loader.py
├── data/                  # Sample input data
│   └── sales_data.csv
├── output/                # Pipeline outputs (gitignored)
│   ├── sales.db
│   └── pipeline.log
├── Dockerfile             # OCI-compliant image
├── docker-compose.yml     # Container orchestration
├── requirements.txt       # Python dependencies
├── requirements-dev.txt   # Dev dependencies
├── setup.cfg              # Linting/testing config
├── .env.example           # Environment template
└── README.md              # This file
```

## 🧪 Testing

```bash
# Run all tests with coverage
docker compose run test

# Or locally
pytest tests/ -v --cov=flexetl --cov-report=term-missing

# Run specific test file
pytest tests/test_extractor.py -v

# Check code quality
flake8 flexetl/ tests/
black --check flexetl/ tests/
mypy flexetl/
```

## 📊 Pipeline Execution Flow

```
1. EXTRACT
   └─> Read data/sales_data.csv
       └─> Load into Pandas DataFrame

2. TRANSFORM
   └─> Filter null values
   └─> Filter invalid quantities (> 0)
   └─> Calculate revenue (quantity * unit_price)
   └─> Aggregate by date + product_id
       └─> Sum quantity and revenue

3. LOAD
   └─> Write to output/sales.db
       └─> Table: daily_product_revenue
   └─> Verify record count
```

## 🔧 Configuration

Phase 1 uses hardcoded parameters. Configuration management comes in Phase 2.

Current settings:
- **Input**: `data/sales_data.csv`
- **Output DB**: `output/sales.db`
- **Output Table**: `daily_product_revenue`
- **Log Level**: INFO (override with `LOG_LEVEL` env var)

## 📝 Logs

Logs are written to:
- **Console**: Real-time output
- **File**: `output/pipeline.log`

```bash
# View logs
tail -f output/pipeline.log

# Or from container
docker compose logs -f pipeline
```

## 🛠️ Development

### Code Quality Standards
- **PEP 8**: Max line length 79, proper formatting
- **Type Hints**: All function signatures annotated
- **Docstrings**: Google-style for all public APIs
- **Test Coverage**: >70% (Phase 1), >80% target (v1.0)

### Running Linters
```bash
flake8 flexetl/ tests/
black flexetl/ tests/
isort flexetl/ tests/
mypy flexetl/
```

## 🗺️ Roadmap

FlexETL follows an agile, phased approach. Each phase is independently releasable:

- **✅ Phase 1 (v0.1.0)**: Working MVP with CSV → Pandas → SQLite
- **Phase 2 (v0.2.0)**: Configuration-driven pipeline (YAML)
- **Phase 3 (v0.3.0)**: Multi-source support (CSV, JSON, REST API)
- **Phase 4 (v0.4.0)**: Data quality & validation
- **Phase 5 (v0.5.0)**: Fault tolerance & retry logic
- **Phase 6 (v0.6.0)**: Orchestration & scheduling
- **Phase 7 (v0.7.0)**: Monitoring & observability
- **Phase 8 (v0.8.0)**: Scalability (large datasets)
- **Phase 9 (v0.9.0)**: Multi-target loading
- **Phase 10 (v1.0.0)**: Security & compliance

See [BRD.md](BRD.md) for detailed requirements.

## 🤝 Contributing

This is a portfolio/learning project. Feedback and suggestions welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Ensure all tests pass and code is PEP 8 compliant
5. Submit a pull request

## 📄 License

See [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built using Python, Pandas, SQLite
- Containerized with Docker (Podman compatible)
- Tested with pytest
- Follows PEP 8 and SOLID principles

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub

---

**FlexETL v0.1.0**
