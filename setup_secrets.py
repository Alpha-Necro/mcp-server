from github import Github
import os
import secrets
from dotenv import load_dotenv
import base64

def generate_webhook_secret():
    """Generate a secure webhook secret."""
    return secrets.token_hex(32)

def setup_secrets():
    load_dotenv()
    token = os.getenv("GITHUB_ACCESS_TOKEN")
    
    if not token:
        print("⚠️ GITHUB_ACCESS_TOKEN not found in .env file!")
        return
    
    g = Github(token)
    
    try:
        repo = g.get_user().get_repo("mcp-server")
        
        # Get existing secrets
        existing_secrets = [secret.name for secret in repo.get_secrets()]
        
        # 1. Set up MCP_GITHUB_TOKEN (use existing token)
        if "MCP_GITHUB_TOKEN" not in existing_secrets:
            print("\nSetting up MCP_GITHUB_TOKEN...")
            repo.create_secret("MCP_GITHUB_TOKEN", token)
            print("✅ MCP_GITHUB_TOKEN configured")
        else:
            print("\n✅ MCP_GITHUB_TOKEN already exists")
        
        # 2. Generate and set up MCP_WEBHOOK_SECRET
        if "MCP_WEBHOOK_SECRET" not in existing_secrets:
            print("\nGenerating new webhook secret...")
            webhook_secret = generate_webhook_secret()
            repo.create_secret("MCP_WEBHOOK_SECRET", webhook_secret)
            print("✅ MCP_WEBHOOK_SECRET configured")
            
            # Save webhook secret to local .env file
            env_path = os.path.join(os.path.dirname(__file__), '.env')
            with open(env_path, 'r') as f:
                env_content = f.read()
            
            if 'GITHUB_WEBHOOK_SECRET=' not in env_content:
                with open(env_path, 'a') as f:
                    f.write(f"\nGITHUB_WEBHOOK_SECRET={webhook_secret}\n")
                print("✅ Webhook secret saved to .env file")
        else:
            print("\n✅ MCP_WEBHOOK_SECRET already exists")
        
        print("\n🎉 All secrets configured successfully!")
        print("\nNext steps:")
        print("1. The secrets are now available in GitHub Actions")
        print("2. Local .env file has been updated with webhook secret")
        print("3. You can now run the deployment workflow")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

if __name__ == "__main__":
    print("Setting up GitHub secrets for MCP Server...")
    setup_secrets()
