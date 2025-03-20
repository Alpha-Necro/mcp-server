from github import Github
import os
from dotenv import load_dotenv

def check_pr_status():
    load_dotenv()
    token = os.getenv("GITHUB_ACCESS_TOKEN")
    g = Github(token)
    
    try:
        repo = g.get_user().get_repo("mcp-server")
        
        # Get PR #2 (GitHub Actions setup)
        pr = repo.get_pull(2)
        
        print("\nPull Request Status")
        print("==================")
        print(f"Title: {pr.title}")
        print(f"Status: {pr.state}")
        print(f"Mergeable: {pr.mergeable}")
        print(f"URL: {pr.html_url}")
        print(f"\nBranch Info:")
        print(f"Base: {pr.base.ref}")
        print(f"Head: {pr.head.ref}")
        
        # Check for any merge conflicts
        if not pr.mergeable:
            print("\n⚠️ This PR has merge conflicts that need to be resolved")
            
        # Check for any reviews
        reviews = list(pr.get_reviews())
        if reviews:
            print("\nReviews:")
            for review in reviews:
                print(f"- {review.user.login}: {review.state}")
        else:
            print("\nNo reviews yet")
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    print("Checking PR status...")
    check_pr_status()
