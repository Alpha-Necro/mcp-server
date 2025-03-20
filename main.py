from fastapi import FastAPI, HTTPException, Depends, status, Header, Request
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List, Dict
import uvicorn
import time
import os
from github_integration import (
    RepoInfo, IssueCreate, PullRequestCreate,
    create_issue, create_pull_request, list_issues,
    get_repo_info, github_config
)

app = FastAPI(
    title="MCP Server",
    description="Mission Control Protocol server for GitHub and Windsurf integration",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Track server start time for uptime monitoring
START_TIME = time.time()

class CommandRequest(BaseModel):
    command: str
    args: Optional[dict] = None

class CommandResponse(BaseModel):
    status: str
    data: Optional[dict] = None
    error: Optional[str] = None

@app.get("/")
async def root():
    """Root endpoint to check if the server is running."""
    return {"status": "active", "message": "MCP Server is running"}

@app.get("/health")
async def health_check() -> Dict:
    """Health check endpoint for container and deployment monitoring."""
    uptime = int(time.time() - START_TIME)
    
    # Check GitHub token
    github_configured = bool(os.getenv("GITHUB_ACCESS_TOKEN"))
    webhook_configured = bool(os.getenv("GITHUB_WEBHOOK_SECRET"))
    
    health_status = {
        "status": "healthy",
        "uptime_seconds": uptime,
        "github_integration": {
            "token_configured": github_configured,
            "webhook_configured": webhook_configured
        },
        "version": "1.0.0"
    }
    
    # Set appropriate status code
    if not (github_configured and webhook_configured):
        health_status["status"] = "degraded"
        return JSONResponse(
            content=health_status,
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE
        )
    
    return health_status

@app.post("/command", response_model=CommandResponse)
async def execute_command(request: CommandRequest):
    try:
        # Here you would implement actual command handling
        return CommandResponse(
            status="success",
            data={"command": request.command, "args": request.args}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

# GitHub Integration Endpoints
@app.post("/github/issues/create")
async def github_create_issue(repo_info: RepoInfo, issue: IssueCreate):
    return await create_issue(repo_info, issue)

@app.post("/github/pr/create")
async def github_create_pr(repo_info: RepoInfo, pr: PullRequestCreate):
    return await create_pull_request(repo_info, pr)

@app.get("/github/issues/list")
async def github_list_issues(repo_info: RepoInfo):
    return await list_issues(repo_info)

@app.get("/github/repo/info")
async def github_get_repo_info(repo_info: RepoInfo):
    return await get_repo_info(repo_info)

@app.post("/github/webhook")
async def github_webhook(
    request: Request,
    x_hub_signature_256: str = Header(None)
):
    payload = await request.body()
    if not github_config.verify_webhook_signature(x_hub_signature_256, payload):
        raise HTTPException(status_code=401, detail="Invalid webhook signature")
    
    event_type = request.headers.get("X-GitHub-Event")
    data = await request.json()
    
    return {
        "status": "success",
        "event": event_type,
        "data": data
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
