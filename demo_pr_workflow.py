from github import Github
import os
from dotenv import load_dotenv

def create_pr_demo():
    load_dotenv()
    token = os.getenv("GITHUB_ACCESS_TOKEN")
    g = Github(token)
    
    # Repository settings
    REPO_NAME = "Computer-Programming101_-JAVA-"  # Using your Java programming repository
    BRANCH_NAME = "demo-pr-branch"
    
    try:
        # Get the repository
        repo = g.get_user().get_repo(REPO_NAME)
        print(f"\nAccessing repository: {repo.full_name}")
        
        # Get the default branch
        default_branch = repo.default_branch
        print(f"Default branch is: {default_branch}")
        
        # Get the default branch's latest commit SHA
        default_branch_ref = repo.get_git_ref(f"heads/{default_branch}")
        base_sha = default_branch_ref.object.sha
        print(f"Base SHA: {base_sha}")
        
        # Create a new branch
        try:
            ref = repo.create_git_ref(f"refs/heads/{BRANCH_NAME}", base_sha)
            print(f"\nCreated new branch: {BRANCH_NAME}")
        except Exception as e:
            print(f"Branch may already exist: {str(e)}")
            ref = repo.get_git_ref(f"heads/{BRANCH_NAME}")
        
        # Create a test file in the new branch
        try:
            content = "# Demo Change\nThis is a test change to demonstrate pull requests."
            repo.create_file(
                "demo/test.md",
                "Add demo file for PR example",
                content,
                branch=BRANCH_NAME
            )
            print("Created test file in new branch")
        except Exception as e:
            print(f"File may already exist: {str(e)}")
        
        # Create a pull request
        pr = repo.create_pull(
            title="Demo Pull Request",
            body="This is a demonstration of creating a pull request using the GitHub API.",
            head=BRANCH_NAME,
            base=default_branch
        )
        
        print("\nPull Request created successfully!")
        print(f"PR URL: {pr.html_url}")
        print(f"PR Number: {pr.number}")
        print(f"PR Status: {pr.state}")
        
        return pr.html_url
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

if __name__ == "__main__":
    print("Creating a demo pull request...")
    pr_url = create_pr_demo()
    if pr_url:
        print("\nYou can view your pull request at the URL above!")
