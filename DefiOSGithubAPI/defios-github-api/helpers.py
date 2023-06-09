from github import Github


def get_resource_no(payload):
    if "issue" in payload.keys():
        url = payload["issue"]["url"]
        resource_no = url.split("issues/")[1]
    elif "pull_request" in payload.keys():
        resource_no = payload["number"]
    return int(resource_no)


def get_issue(github_app, payload):
    owner = payload["repository"]["owner"]["login"]
    repo_name = payload["repository"]["name"]
    git_connection = Github(app_auth=github_app)
    repo = git_connection.get_repo(f"{owner}/{repo_name}")
    resource_no = get_resource_no(payload)
    issue = repo.get_issue(number=resource_no)
    return issue


def get_pr(github_app, payload):
    owner = payload["repository"]["owner"]["login"]
    repo_name = payload["repository"]["name"]
    git_connection = Github(app_auth=github_app)
    repo = git_connection.get_repo(f"{owner}/{repo_name}")
    resource_no = get_resource_no(payload)
    pr = repo.get_pull(number=resource_no)
    return pr


def create_comment(resource, comment):
    try:
        resource.create_comment(comment)
    except:
        resource = resource.as_issue()
        resource.create_comment(comment)


def read_markdown(file_path):
    with open(file_path, "r") as f:
        text = f.read()
    return text


def create_issue_comment(github_app, payload, comment_path):
    comment = read_markdown(comment_path)
    issue = get_issue(github_app, payload)
    create_comment(issue, comment)


def create_pr_comment(github_app, payload, comment_path):
    comment = read_markdown(comment_path)
    pr = get_pr(github_app, payload)
    create_comment(pr, comment)
