# Deployment Notes

This file contains guidance for deploying the Real-Time Shopping Personal Assistant.

- Containerization: Provide a `Dockerfile` (sample below) and push to a registry.
- Cloud Run / Agent Engine: Use a small CPU memory-optimized instance. Persist vector store to a cloud storage volume or managed vector DB.
- Environment: Store secrets in Secret Manager and inject via environment variables.

Sample Dockerfile snippet

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
CMD ["python", "main.py"]
```

Recommended runtime options
- Use concurrency for event ingestion (async loop).
- Configure liveness/readiness probes for long-running loops.
- Use persistent volume for `VECTOR_STORE_PATH` or use a managed vector DB.

Observability
- Export `metrics.csv` to a central store or use Prometheus exporter.
- Forward structured logs (JSON) to a logging backend (Cloud Logging/Datadog).

Security
- Never store API keys in code. Use environment variables/secret manager.
- Use least-privilege credentials for external APIs.

Scaling
- Run multiple orchestrator instances and partition events by user_id or queue.
- Use a message queue (Pub/Sub, SQS) for large-scale ingestion.
