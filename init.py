import os, sys, argparse
from github import Github

def get_repo(gitHubClient, repoName, githubOrg):
    repo = gitHubClient.get_repo("{owner}/{repo_name}".format(owner=githubOrg, repo_name=repoName))
    return repo


def create_webhook(repo, host):
    ENDPOINT = "github-webhook/"
    EVENTS = ["push", "pull_request","release"]

    config = {
        "url": "https://{host}/{endpoint}".format(host=host, endpoint=ENDPOINT),
        "content_type": "json"
    }

    repo.create_hook("web", config, EVENTS, active=True)

def protect_branch(repo):
    master_branch = repo.get_branch("master")
    master_branch.edit_protection(strict=True, contexts=['continuous-integration/jenkins/pr-merge'])


def main():
    githubToken = os.environ.get('GITHUB_API_TOKEN')
    gitHubClient = Github(githubToken)
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--orgName", help="The name of the github organization the repo lives in.")
    parser.add_argument("-r", "--repoName", help="The name of the github repository to configure.")
    parser.add_argument("-j", "--jenkinsUrl", help="The URL of the jenkins server the webhook will post to")
    parser.add_argument("-t", "--testOrg", action='store_true', help="If specified redventures-incubator org will be used.")
    args = parser.parse_args()

    repo = get_repo(gitHubClient, args.repoName, args.orgName)

    create_webhook(repo, args.jenkinsUrl)

    protect_branch(repo)

if __name__ == "__main__":
    main()
