from github import Github
import os
from dotenv import load_dotenv

def create_deployment_pr():
    load_dotenv()
    token = os.getenv("GITHUB_ACCESS_TOKEN")
    g = Github(token)
    
    try:
        repo = g.get_user().get_repo("mcp-server")
        
        # Create pull request
        pr = repo.create_pull(
            title="Add Docker and Deployment Configuration",
            body="""# Docker and Deployment Setup

This PR adds comprehensive deployment configuration for the MCP server:

## Added Features
1. **Docker Support**
   - Dockerfile for containerization
   - docker-compose.yml for local development
   - Multi-stage build optimization
   - Non-root user security

2. **Deployment Configuration**
   - GitHub Container Registry integration
   - Environment configuration management
   - Health check endpoint
   - Container readiness checks

3. **Documentation**
   - Added DEPLOYMENT.md with setup instructions
   - Server monitoring guidelines
   - Rollback procedures
   - Troubleshooting guide

4. **GitHub Actions Updates**
   - Docker build and push workflow
   - Container registry integration
   - Deployment secrets configuration

## Security Considerations
- Non-root container user
- Environment-based secrets management
- Health check endpoint for monitoring
- Container security best practices

## Testing Instructions
1. Build locally:
   ```bash
   docker-compose up --build
   ```

2. Test health endpoint:
   ```bash
   curl http://localhost:8000/health
   ```

Please review the implementation and deployment configuration.""",
            head="setup-deployment",
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
    print("Creating pull request for deployment setup...")
    pr_url = create_deployment_pr()
    if pr_url:
        print("\nYou can review and merge the PR at the URL above.")
