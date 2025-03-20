# MCP Server

A Mission Control Protocol server for GitHub and Windsurf integration.

## Setup

1. Configure GitHub integration:
   - Copy `.env.example` to `.env`
   - Add your GitHub access token and webhook secret

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the server:
```bash
python main.py
```

The server will start on `http://localhost:8000`

## API Endpoints

### Core Endpoints
- `GET /` - Check server status
- `POST /command` - Execute MCP commands

### GitHub Integration
- `POST /github/issues/create` - Create a new GitHub issue
- `POST /github/pr/create` - Create a new pull request
- `GET /github/issues/list` - List open issues in a repository
- `GET /github/repo/info` - Get repository information
- `POST /github/webhook` - GitHub webhook endpoint for events

## GitHub Integration

### Authentication
Set your GitHub access token in the `.env` file:
```
GITHUB_ACCESS_TOKEN=your_github_token_here
GITHUB_WEBHOOK_SECRET=your_webhook_secret_here
```

### Example Usage

```bash
# Create an issue
curl -X POST http://localhost:8000/github/issues/create \
  -H "Content-Type: application/json" \
  -d '{"repo_info": {"owner": "username", "repo": "repo-name"}, 
       "issue": {"title": "New Issue", "body": "Issue description"}}
```

## Development

The server uses FastAPI with automatic reload enabled for development. API documentation is available at `/docs`.
