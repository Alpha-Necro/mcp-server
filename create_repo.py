from github import Github
import os
from dotenv import load_dotenv

def create_github_repository():
    load_dotenv()
    token = os.getenv("GITHUB_ACCESS_TOKEN")
    g = Github(token)
    
    try:
        # Create repository
        user = g.get_user()
        repo = user.create_repo(
            name="mcp-server",
            description="Mission Control Protocol (MCP) server for GitHub and Windsurf integration",
            homepage="",
            private=False,
            has_issues=True,
            has_wiki=True,
            has_downloads=True,
            auto_init=True
        )
        
        print(f"\nRepository created successfully!")
        print(f"Repository URL: {repo.html_url}")
        print(f"Clone URL: {repo.clone_url}")
        
        # Set up branch protection rules
        main_branch = repo.get_branch("main")
        main_branch.edit_protection(
            required_approving_review_count=1,
            enforce_admins=True,
            dismiss_stale_reviews=True,
            require_code_owner_reviews=False
        )
        print("\nBranch protection rules set up for main branch")
        
        return repo.clone_url
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

if __name__ == "__main__":
    print("Creating new GitHub repository for MCP server...")
    clone_url = create_github_repository()
    if clone_url:
        print("\nNext steps:")
        print("1. Add remote origin")
        print("2. Push initial code")
        print("3. Set up GitHub Actions")
