from github import Github
from fastapi import HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
import os
import hmac
import hashlib
from dotenv import load_dotenv

load_dotenv()

class GitHubConfig:
    def __init__(self):
        self.access_token = os.getenv("GITHUB_ACCESS_TOKEN")
        self.webhook_secret = os.getenv("GITHUB_WEBHOOK_SECRET")
        if not self.access_token:
            raise ValueError("GitHub access token not found in environment")
        self.client = Github(self.access_token)

    def verify_webhook_signature(self, signature: str, payload: bytes) -> bool:
        if not self.webhook_secret:
            return False
        expected_signature = 'sha256=' + hmac.new(
            self.webhook_secret.encode('utf-8'),
            payload,
            hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(expected_signature, signature)

class RepoInfo(BaseModel):
    owner: str
    repo: str
    branch: Optional[str] = "main"

class IssueCreate(BaseModel):
    title: str
    body: str
    labels: Optional[List[str]] = None

class PullRequestCreate(BaseModel):
    title: str
    body: str
    head: str
    base: str = "main"

github_config = GitHubConfig()

def get_github_client():
    return github_config.client

async def create_issue(repo_info: RepoInfo, issue: IssueCreate, client: Github = Depends(get_github_client)):
    try:
        repo = client.get_repo(f"{repo_info.owner}/{repo_info.repo}")
        created_issue = repo.create_issue(
            title=issue.title,
            body=issue.body,
            labels=issue.labels
        )
        return {
            "id": created_issue.number,
            "url": created_issue.html_url,
            "status": "created"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def create_pull_request(repo_info: RepoInfo, pr: PullRequestCreate, client: Github = Depends(get_github_client)):
    try:
        repo = client.get_repo(f"{repo_info.owner}/{repo_info.repo}")
        created_pr = repo.create_pull(
            title=pr.title,
            body=pr.body,
            head=pr.head,
            base=pr.base
        )
        return {
            "id": created_pr.number,
            "url": created_pr.html_url,
            "status": "created"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def list_issues(repo_info: RepoInfo, client: Github = Depends(get_github_client)):
    try:
        repo = client.get_repo(f"{repo_info.owner}/{repo_info.repo}")
        issues = repo.get_issues(state="open")
        return [{
            "id": issue.number,
            "title": issue.title,
            "url": issue.html_url,
            "state": issue.state,
            "created_at": issue.created_at.isoformat()
        } for issue in issues]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def get_repo_info(repo_info: RepoInfo, client: Github = Depends(get_github_client)):
    try:
        repo = client.get_repo(f"{repo_info.owner}/{repo_info.repo}")
        return {
            "name": repo.name,
            "full_name": repo.full_name,
            "description": repo.description,
            "default_branch": repo.default_branch,
            "stars": repo.stargazers_count,
            "forks": repo.forks_count,
            "open_issues": repo.open_issues_count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
