# Docker Quick Start

## Build and Run with Docker

### 1. Build the Docker image

```bash
docker build -t llm-judge-api .
```

### 2. Run with environment variables

```bash
docker run -d \
  -p 8000:8000 \
  -e OPENAI_API_KEY=your_key_here \
  -e ANTHROPIC_API_KEY=your_key_here \
  -e ENVIRONMENT=production \
  --name llm-judge-api \
  llm-judge-api
```

### 3. Or use docker-compose

```bash
# Create .env file first with your API keys
docker-compose up -d
```

### 4. Check logs

```bash
docker logs -f llm-judge-api
```

### 5. Stop the container

```bash
docker stop llm-judge-api
```

## Using Docker Compose (Recommended)

### Start services
```bash
docker-compose up -d
```

### View logs
```bash
docker-compose logs -f
```

### Stop services
```bash
docker-compose down
```

### Rebuild after changes
```bash
docker-compose up -d --build
```

## Environment Variables

Pass these when running the container:

- `OPENAI_API_KEY` - Your OpenAI API key
- `ANTHROPIC_API_KEY` - Your Anthropic API key
- `ENVIRONMENT` - Set to "production" for production
- `LOG_LEVEL` - Log level (INFO, DEBUG, WARNING, ERROR)
- `ALLOWED_ORIGINS` - Comma-separated CORS origins

## Health Check

The Docker container includes a health check that runs every 30 seconds:

```bash
docker ps  # Check health status
```

## Production Deployment

### Deploy to AWS ECS, Google Cloud Run, or Azure Container Apps

1. Build and push to container registry:
```bash
docker build -t your-registry/llm-judge-api:latest .
docker push your-registry/llm-judge-api:latest
```

2. Deploy using platform-specific tools

3. Set environment variables in the platform's configuration

## Troubleshooting

### Container won't start
```bash
docker logs llm-judge-api
```

### Check if container is running
```bash
docker ps -a
```

### Enter container for debugging
```bash
docker exec -it llm-judge-api /bin/bash
```

### Remove and rebuild
```bash
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```
