# Container Compatibility Guide

This guide provides detailed information about running FlexETL with Docker and Podman, ensuring cross-platform compatibility.

## 🎯 OCI Compliance

FlexETL container images follow the **Open Container Initiative (OCI)** standard, making them compatible with any OCI-compliant runtime including:
- Docker
- Podman
- containerd
- CRI-O

## 🐳 Docker Setup

### Installation

**Linux:**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

**macOS:**
```bash
brew install --cask docker
# Or download Docker Desktop from docker.com
```

**Windows:**
Download Docker Desktop from [docker.com](https://www.docker.com/)

### Docker Compose

Modern Docker includes Compose v2:
```bash
docker compose version
```

If using older Docker Compose v1:
```bash
# Replace 'docker compose' with 'docker-compose' in all commands
docker-compose up pipeline
```

### Running FlexETL

```bash
# Build image
docker compose build

# Run pipeline
docker compose up pipeline

# Run tests
docker compose run test

# Run in background
docker compose up -d pipeline

# View logs
docker compose logs -f pipeline

# Stop containers
docker compose down
```

## 🦭 Podman Setup

### Why Podman?

- **Daemonless**: No background service required
- **Rootless**: Better security, runs as regular user
- **Docker-compatible**: Drop-in replacement for most use cases
- **Open Source**: Fully open-source, no commercial licensing

### Installation

**Linux (Fedora/RHEL/CentOS):**
```bash
sudo dnf install podman podman-compose
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install podman podman-compose
```

**macOS:**
```bash
brew install podman podman-compose

# Initialize Podman machine
podman machine init
podman machine start
```

**Windows:**
Download from [podman.io](https://podman.io/)

### Running FlexETL with Podman

#### Option 1: Using podman-compose (Recommended)

```bash
# Build image
podman-compose build

# Run pipeline
podman-compose up pipeline

# Run tests
podman-compose run test

# Cleanup
podman-compose down
```

#### Option 2: Using podman directly

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
  flexetl:latest \
  sh -c "pip install -r requirements-dev.txt && pytest tests/ -v"

# Interactive shell
podman run -it --rm \
  -v ./flexetl:/app/flexetl \
  flexetl:latest \
  /bin/bash
```

## 🔄 Command Equivalents

| Docker | Podman |
|--------|--------|
| `docker compose up` | `podman-compose up` |
| `docker compose build` | `podman-compose build` |
| `docker compose run` | `podman-compose run` |
| `docker compose down` | `podman-compose down` |
| `docker build` | `podman build` |
| `docker run` | `podman run` |
| `docker ps` | `podman ps` |
| `docker images` | `podman images` |
| `docker logs` | `podman logs` |

For most cases, you can use **alias docker=podman** in your shell!

## 🛠️ Volume Mounting

### Docker
```bash
docker compose up pipeline
# Volumes defined in docker-compose.yml automatically mounted
```

### Podman
```bash
podman-compose up pipeline
# Works identically to Docker

# Or with podman directly:
podman run -v ./data:/app/data:ro -v ./output:/app/output flexetl:latest
```

**Important**: Use relative paths (`./`) or absolute paths for volume mounts.

## 🔐 Permissions

### Docker
Runs as user `flexetl` (UID 1000) inside container.

### Podman (Rootless)
- Runs without root privileges
- User mapping: Container UID 1000 → Your host UID
- Output files owned by your user automatically

**If you encounter permission issues:**

```bash
# Docker: Fix output directory permissions
sudo chown -R $USER:$USER output/

# Podman: Usually no issues due to user namespaces
```

## 🌐 Networking

### Docker
Uses bridge network (`flexetl-network`) defined in docker-compose.yml.

### Podman
Compatible with Docker networking:
```bash
podman-compose up  # Uses same network config
```

For multi-container setups (Phase 6+):
```bash
# Docker
docker compose up scheduler pipeline

# Podman
podman-compose up scheduler pipeline
```

## 🏗️ Image Building

### Multi-Stage Builds (Phase 2+)

Both Docker and Podman support multi-stage builds:

```dockerfile
# Build stage
FROM python:3.9-slim AS builder
RUN pip install --user ...

# Runtime stage
FROM python:3.9-slim
COPY --from=builder ...
```

### Build Arguments

```bash
# Docker
docker compose build --build-arg PYTHON_VERSION=3.11

# Podman
podman-compose build --build-arg PYTHON_VERSION=3.11
```

## 🧪 Testing Compatibility

FlexETL CI/CD pipeline tests on both runtimes:

```bash
# Test with Docker
docker compose run test

# Test with Podman
podman-compose run test
```

Both should produce identical results.

## 🐛 Troubleshooting

### Issue: "permission denied" on output files

**Docker:**
```bash
sudo chown -R $USER:$USER output/
```

**Podman:**
Usually not an issue. If it occurs:
```bash
podman unshare chown -R 1000:1000 output/
```

### Issue: "compose not found"

**Docker:**
```bash
# Install Compose v2
sudo apt-get install docker-compose-plugin
```

**Podman:**
```bash
# Install podman-compose
pip3 install podman-compose
```

### Issue: Volume mount not working

**Both:**
Ensure you're in the project root directory:
```bash
cd /path/to/FlexETL
docker compose up  # or podman-compose up
```

### Issue: Port already in use (Phase 6+)

**Docker:**
```bash
docker compose down
docker ps -a  # Check for hanging containers
```

**Podman:**
```bash
podman-compose down
podman ps -a
```

### Issue: Podman machine not running (macOS/Windows)

```bash
podman machine start
podman machine list
```

## 📊 Performance Comparison

| Aspect | Docker | Podman |
|--------|--------|--------|
| Build Speed | Fast | Fast (similar) |
| Startup Time | ~1-2s | ~1-2s |
| Memory Usage | Slightly higher | Slightly lower |
| Security | Good | Better (rootless) |
| Ecosystem | Larger | Growing |

For FlexETL Phase 1, performance is virtually identical.

## 🔒 Security Best Practices

Both Docker and Podman in FlexETL:

✅ Non-root user execution
✅ Minimal base image (python:3.9-slim)
✅ No secrets in image layers
✅ Read-only data mounts
✅ Isolated network
✅ Security scanning compatible

```bash
# Scan image with Trivy
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/trivy:latest image flexetl:latest

# With Podman
podman run --rm -v $(pwd):/scan \
  aquasec/trivy:latest image flexetl:latest
```

## 🚀 Production Deployment

### Docker Swarm
```bash
docker stack deploy -c docker-compose.yml flexetl
```

### Kubernetes (Future)
Both Docker and Podman images work with Kubernetes:
```bash
kubectl create deployment flexetl --image=flexetl:latest
```

### Podman with systemd (Linux)
```bash
# Generate systemd unit file
podman generate systemd --name flexetl-pipeline > \
  ~/.config/systemd/user/flexetl.service

systemctl --user enable flexetl
systemctl --user start flexetl
```

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Podman Documentation](https://docs.podman.io/)
- [OCI Specification](https://opencontainers.org/)
- [Docker to Podman Migration](https://podman.io/blogs/2021/09/06/podman-3.3.1.html)

## 🎓 Learning Path

**New to containers?** Start with Docker:
1. Run FlexETL with `docker compose up`
2. Understand basic commands
3. Learn about images and containers

**Want better security?** Try Podman:
1. Install Podman
2. Run same commands with `podman-compose`
3. Enjoy rootless containers!

---

**Questions or issues?** Open an issue on GitHub with:
- Container runtime (Docker/Podman) and version
- Operating system
- Error message or unexpected behavior
- Steps to reproduce
