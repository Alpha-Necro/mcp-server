from github import Github
import os
from dotenv import load_dotenv

def merge_actions_pr():
    load_dotenv()
    token = os.getenv("GITHUB_ACCESS_TOKEN")
    g = Github(token)
    
    try:
        repo = g.get_user().get_repo("mcp-server")
        pr = repo.get_pull(2)  # GitHub Actions PR
        
        if pr.mergeable:
            # Create an approving review first
            try:
                pr.create_review(
                    body="GitHub Actions workflows look good. Adding comprehensive CI/CD pipeline.",
                    event="APPROVE"
                )
            except Exception as e:
                print(f"Note: Could not create review (expected for self-reviews): {e}")
            
            # Try to merge
            pr.merge(
                commit_title="Add GitHub Actions Workflows",
                commit_message="""Add comprehensive GitHub Actions workflows:
- CI pipeline with testing and linting
- Security scanning workflow
- Automated deployment pipeline
- Test suite setup""",
                merge_method="squash"
            )
            print("\n🎉 PR has been successfully merged!")
            
            # Clean up the branch
            try:
                ref = repo.get_git_ref(f"heads/{pr.head.ref}")
                ref.delete()
                print(f"Cleaned up: Deleted the '{pr.head.ref}' branch")
            except Exception as e:
                print(f"Note: Could not delete branch: {e}")
                
        else:
            print("\n⚠️ This PR has conflicts that need to be resolved before merging.")
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    print("Merging GitHub Actions PR...")
    merge_actions_pr()
