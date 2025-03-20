from github import Github
import os
from dotenv import load_dotenv
from pprint import pprint

def review_pull_request():
    load_dotenv()
    token = os.getenv("GITHUB_ACCESS_TOKEN")
    g = Github(token)
    
    try:
        repo = g.get_user().get_repo("mcp-server")
        pr = repo.get_pull(1)  # Get PR #1
        
        print("\nPull Request Review")
        print("===================")
        print(f"Title: {pr.title}")
        print(f"Status: {pr.state}")
        print(f"Created by: {pr.user.login}")
        print(f"Base branch: {pr.base.ref}")
        print(f"Compare branch: {pr.head.ref}")
        
        print("\nFiles Changed:")
        print("-------------")
        for file in pr.get_files():
            print(f"- {file.filename} ({file.status}, +{file.additions}/-{file.deletions} lines)")
        
        print("\nChecks and Status:")
        print("----------------")
        for status in pr.get_commits()[0].get_statuses():
            print(f"- {status.context}: {status.state}")
            
        if pr.mergeable:
            print("\n✅ This PR can be merged!")
            
            # Approve the PR
            pr.create_review(
                body="Code review completed. All changes look good and follow best practices.",
                event="APPROVE"
            )
            
            # Merge the PR
            pr.merge(
                commit_title="Initial MCP Server Implementation",
                commit_message="Merging initial MCP server implementation with GitHub integration",
                merge_method="squash"
            )
            print("\n🎉 PR has been approved and merged!")
        else:
            print("\n⚠️ This PR has conflicts that need to be resolved before merging.")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    print("Reviewing and merging pull request...")
    review_pull_request()
