from github import Github
import os
from dotenv import load_dotenv

def test_github_connection():
    load_dotenv()
    token = os.getenv("GITHUB_ACCESS_TOKEN")
    
    try:
        # Initialize GitHub client
        g = Github(token)
        
        # Get the authenticated user
        user = g.get_user()
        print(f"Successfully connected as: {user.login}")
        
        # List some repositories
        print("\nYour repositories:")
        for repo in user.get_repos()[:5]:  # Show first 5 repos
            print(f"- {repo.full_name}")
            
        return True
    except Exception as e:
        print(f"Error connecting to GitHub: {str(e)}")
        return False

if __name__ == "__main__":
    test_github_connection()
