from github import Github
import os
from dotenv import load_dotenv

def create_actions_pr():
    load_dotenv()
    token = os.getenv("GITHUB_ACCESS_TOKEN")
    g = Github(token)
    
    try:
        repo = g.get_user().get_repo("mcp-server")
        
        # Create pull request
        pr = repo.create_pull(
            title="Add GitHub Actions Workflows",
            body="""# GitHub Actions Setup

This PR adds comprehensive CI/CD workflows:

## Added Workflows
1. **CI Pipeline (`ci.yml`)**
   - Runs tests on Python 3.9-3.12
   - Code formatting (Black)
   - Import sorting (isort)
   - Linting (flake8)
   - Test coverage reporting

2. **Security Scanning (`security.yml`)**
   - Weekly security scans
   - Dependency vulnerability checks
   - CodeQL analysis
   - Bandit security scanner

3. **Deployment (`deploy.yml`)**
   - Automated releases
   - Package building
   - Version tagging

## Testing Setup
- Added pytest configuration
- Created initial test suite
- Added test dependencies

## Changes
- Created `.github/workflows/` directory with 3 workflow files
- Added `tests/` directory with initial test suite
- Updated `requirements.txt` with testing dependencies

Please review the implementation and provide feedback.""",
            head="setup-github-actions",
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
    print("Creating pull request for GitHub Actions setup...")
    pr_url = create_actions_pr()
    if pr_url:
        print("\nYou can review and merge the PR at the URL above.")
