from github import Github
import os
from dotenv import load_dotenv

def update_branch_protection():
    load_dotenv()
    token = os.getenv("GITHUB_ACCESS_TOKEN")
    g = Github(token)
    
    try:
        repo = g.get_user().get_repo("mcp-server")
        branch = repo.get_branch("main")
        
        # Update branch protection to be less strict for initial setup
        branch.edit_protection(
            required_approving_review_count=0,  # Remove review requirement temporarily
            enforce_admins=False,  # Allow admins to merge
            dismiss_stale_reviews=True,
            require_code_owner_reviews=False
        )
        print("\n✅ Branch protection rules updated")
        return True
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("Updating branch protection rules...")
    update_branch_protection()
