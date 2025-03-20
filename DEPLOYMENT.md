# MCP Server Deployment Guide

## Prerequisites
- Docker and Docker Compose installed on your deployment server
- GitHub account with access to GitHub Container Registry (GHCR)
- GitHub Personal Access Token with required permissions

## GitHub Actions Secrets Setup

1. Go to your repository settings: `https://github.com/Alpha-Necro/mcp-server/settings/secrets/actions`
2. Add the following secrets:
   - `MCP_GITHUB_TOKEN`: Your GitHub Personal Access Token (already configured)
   - `MCP_WEBHOOK_SECRET`: A secure webhook secret for GitHub events

## Local Development

```bash
# Build and run locally
docker-compose up --build

# Run in detached mode
docker-compose up -d
```

## Production Deployment

The MCP server is deployed as a Docker container via GitHub Container Registry.

### Initial Server Setup

1. Install Docker on your server:
   ```bash
   curl -fsSL https://get.docker.com | sh
   ```

2. Login to GitHub Container Registry:
   ```bash
   echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin
   ```

3. Create a deployment directory:
   ```bash
   mkdir -p /opt/mcp-server
   cd /opt/mcp-server
   ```

4. Create environment file:
   ```bash
   cat > .env << EOL
   GITHUB_ACCESS_TOKEN=your_github_token
   GITHUB_WEBHOOK_SECRET=your_webhook_secret
   EOL
   ```

### Deployment Process

The GitHub Actions workflow will:
1. Build the Docker image
2. Push to GitHub Container Registry
3. Create a new release
4. Generate deployment configuration

To deploy manually:
```bash
# Pull the latest image
docker pull ghcr.io/alpha-necro/mcp-server:latest

# Run the container
docker run -d \
  --name mcp-server \
  --restart unless-stopped \
  -p 8000:8000 \
  --env-file .env \
  ghcr.io/alpha-necro/mcp-server:latest
```

### Health Check

The server includes a health check endpoint at `/health`. Monitor it with:
```bash
curl http://localhost:8000/health
```

### Updating

To update to a new version:
```bash
# Pull the new image
docker pull ghcr.io/alpha-necro/mcp-server:latest

# Stop the current container
docker stop mcp-server

# Remove the old container
docker rm mcp-server

# Start a new container
docker run -d \
  --name mcp-server \
  --restart unless-stopped \
  -p 8000:8000 \
  --env-file .env \
  ghcr.io/alpha-necro/mcp-server:latest
```

## Monitoring

Monitor the server logs:
```bash
# View logs
docker logs mcp-server

# Follow logs
docker logs -f mcp-server
```

## Troubleshooting

1. If the container fails to start:
   ```bash
   docker logs mcp-server
   ```

2. Check container status:
   ```bash
   docker ps -a | grep mcp-server
   ```

3. Verify environment variables:
   ```bash
   docker exec mcp-server env
   ```

## Rollback

To rollback to a previous version:
```bash
# List available versions
docker images ghcr.io/alpha-necro/mcp-server

# Pull specific version
docker pull ghcr.io/alpha-necro/mcp-server:specific-tag

# Stop and remove current container
docker stop mcp-server
docker rm mcp-server

# Start container with specific version
docker run -d \
  --name mcp-server \
  --restart unless-stopped \
  -p 8000:8000 \
  --env-file .env \
  ghcr.io/alpha-necro/mcp-server:specific-tag
```
