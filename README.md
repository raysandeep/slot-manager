# Slot Manager

Slot Manager predicts Livekit egress load and scales the deployment replicas.
It polls upcoming interviews from two databases and active calls from Redis,
calculates required resources, and scales a Kubernetes deployment accordingly.
It also exposes an API endpoint to check available slots.

## Running

1. Copy `.env.template` to `.env` and fill in required environment variables.
2. Build and run Docker image:

```bash
docker build -t slot-manager .
docker run --env-file .env slot-manager
```

The service listens on port `8000`.
