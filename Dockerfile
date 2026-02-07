# FlexETL Phase 1 - OCI-compliant container image
# Supports both Docker and Podman

FROM python:3.9-slim

LABEL maintainer="Ajith" \
      version="0.1.0" \
      description="FlexETL - Container-native ETL framework"

WORKDIR /app

RUN useradd -m -u 1000 flexetl && \
    chown -R flexetl:flexetl /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY flexetl/ ./flexetl/
COPY data/ ./data/

RUN mkdir -p output && \
    chown -R flexetl:flexetl /app

USER flexetl

CMD ["python", "-m", "flexetl.main"]
