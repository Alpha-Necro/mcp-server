from github import Github
import os
from dotenv import load_dotenv

def merge_pull_request():
    load_dotenv()
    token = os.getenv("GITHUB_ACCESS_TOKEN")
    g = Github(token)
    
    try:
        repo = g.get_user().get_repo("mcp-server")
        pr = repo.get_pull(1)
        
        if pr.mergeable:
            pr.merge(
                commit_title="Initial MCP Server Implementation",
                commit_message="""Merging initial MCP server implementation with:
- FastAPI REST API
- GitHub Integration
- Command execution
- Security features
- Full documentation""",
                merge_method="squash"
            )
            print("\n🎉 PR has been successfully merged!")
            print(f"View the merged code at: {repo.html_url}")
            
            # Delete the feature branch since we don't need it anymore
            ref = repo.get_git_ref(f"heads/{pr.head.ref}")
            ref.delete()
            print(f"\nCleaned up: Deleted the '{pr.head.ref}' branch")
        else:
            print("\n⚠️ This PR has conflicts that need to be resolved before merging.")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    print("Merging pull request...")
    merge_pull_request()
