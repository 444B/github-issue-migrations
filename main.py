from github import Github
import time

# Initialize GitHub with your token
g = Github("API_TOKEN_HERE")

source_repo = g.get_repo("jrieke/streamlit-analytics")
target_repo = g.get_repo("444B/streamlit-analytics2")

def migrate_issues(source_repo, target_repo):
    issues = source_repo.get_issues(state='all', sort='created')
    
    for issue in issues:
        # Check if issue is a pull request
        if issue.pull_request is not None:
            print(f"Skipping PR: {issue.title}")
            continue  # Skip pull requests
        
        # Create a new issue in the target repository
        new_issue = target_repo.create_issue(
            title=issue.title,
            body=f"Original issue by {issue.user.login} on {issue.created_at}\n\n{issue.body}",
            labels=[label.name for label in issue.get_labels()]
        )
        print(f"Issue created: {new_issue.title}")
        
        # Migrate comments
        comments = issue.get_comments()
        for comment in comments:
            new_issue.create_comment(f"Comment by {comment.user.login} on {comment.created_at}\n\n{comment.body}")
            print(f"Comment added to {new_issue.title}")
        
        # GitHub API rate limiting
        time.sleep(1)  # Be respectful of GitHub's API rate limits

migrate_issues(source_repo, target_repo)
