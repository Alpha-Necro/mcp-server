from github import Github
import os
from dotenv import load_dotenv

def create_initial_pr():
    load_dotenv()
    token = os.getenv("GITHUB_ACCESS_TOKEN")
    g = Github(token)
    
    try:
        repo = g.get_user().get_repo("mcp-server")
        
        # Create pull request
        pr = repo.create_pull(
            title="Initial MCP Server Implementation",
            body="""# Initial MCP Server Setup

This PR includes the complete implementation of the MCP server with:

## Features
- FastAPI-based REST API
- GitHub Integration (issues, PRs, webhooks)
- Command execution endpoint
- CORS support
- Development mode with auto-reload

## Security
- Environment-based configuration
- Branch protection rules
- OAuth2 with JWT support

## Documentation
- Complete API documentation
- Setup instructions
- Usage examples

Please review the implementation and provide feedback.""",
            head="initial-setup",
            base="main"
        )
        
        print(f"\nPull Request created successfully!")
        print(f"PR URL: {pr.html_url}")
        print(f"PR Number: {pr.number}")
        
        return pr.html_url
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

if __name__ == "__main__":
    print("Creating pull request for initial MCP server implementation...")
    pr_url = create_initial_pr()
    if pr_url:
        print("\nYou can review and merge the PR at the URL above.")
