from github import Github
import os
from dotenv import load_dotenv

def merge_deployment_pr():
    load_dotenv()
    token = os.getenv("GITHUB_ACCESS_TOKEN")
    g = Github(token)
    
    try:
        repo = g.get_user().get_repo("mcp-server")
        pr = repo.get_pull(3)  # Deployment PR
        
        if pr.mergeable:
            # Try to merge
            pr.merge(
                commit_title="Add Docker and Deployment Configuration",
                commit_message="""Add comprehensive deployment setup:
- Docker containerization
- GitHub Container Registry integration
- Health check endpoint
- Deployment documentation
- Environment configuration""",
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
    print("Merging deployment PR...")
    merge_deployment_pr()
