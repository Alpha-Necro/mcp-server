import requests
import json

def create_pull_request():
    # The URL of our local MCP server
    url = "http://localhost:8000/github/pr/create"
    
    # Data for the pull request
    data = {
        "repo_info": {
            "owner": "Alpha-Necro",  # Your GitHub username
            "repo": "mcoc"  # One of your repositories
        },
        "title": "Example Pull Request",
        "body": "This is a test pull request created via the MCP server to demonstrate how PRs work.",
        "head": "feature-branch",  # The branch containing your changes
        "base": "main"            # The branch you want to merge into
    }
    
    # Send the request to create a PR
    try:
        response = requests.post(url, json=data)
        print("\nRequest sent to MCP server...")
        print(f"Status Code: {response.status_code}")
        print("\nResponse:")
        print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    print("Creating a pull request through the MCP server...")
    create_pull_request()
