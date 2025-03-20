from fastapi.testclient import TestClient
from main import app
import pytest
from unittest.mock import patch

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "active", "message": "MCP Server is running"}

def test_command_endpoint():
    test_command = {
        "command": "test",
        "args": {"param": "value"}
    }
    response = client.post("/command", json=test_command)
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["data"]["command"] == "test"

@patch('github_integration.Github')
def test_github_repo_info(mock_github):
    # Mock GitHub API response
    mock_repo = type('MockRepo', (), {
        'name': 'test-repo',
        'full_name': 'test-user/test-repo',
        'description': 'Test repository',
        'default_branch': 'main',
        'stargazers_count': 0,
        'forks_count': 0,
        'open_issues_count': 0
    })
    
    mock_github.return_value.get_repo.return_value = mock_repo
    
    response = client.get("/github/repo/info", 
                         json={"owner": "test-user", "repo": "test-repo"})
    assert response.status_code == 200
    assert response.json()["name"] == "test-repo"
