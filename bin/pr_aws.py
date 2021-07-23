import boto3
import argparse
from tabulate import tabulate
import pandas as pd
from flask import Flask, render_template
from IPython.core.display import display, HTML

app = Flask(__name__)


@app.route("/")
def get_repos():

    pullRequests = []

    resp = client.list_repositories()
    repositories = resp['repositories']
    # print(repositories)
    # for r in repositories:
    #     r['pr_link'] = "http://localhost/prs/" + r['repositoryName']

    def make_clickable(url, name):
        return '<a href="prs/{}" rel="noopener noreferrer" target="_blank">{}</a>'.format(url, name)

    df = pd.DataFrame(repositories)
    df['clickable_url'] = df.apply(lambda x: make_clickable(x['repositoryName'], x['repositoryName']), axis=1)
    # df.set_index('repositoryName')
    # df = df.fillna(' ').T
    # df = df.transpose()
    return df.to_html(escape=False)


@app.route("/prs/<repositoryName>")
def get_prs(repositoryName):
    pullRequests = []
    resp = client.list_pull_requests(
        repositoryName=repositoryName,
        pullRequestStatus='OPEN',
    )
    pullRequestIds = resp['pullRequestIds']
    if not pullRequestIds:
        return "NO PRS for this Repo"

    for p in pullRequestIds:
        pullRequests.append(p)

    all_prs = []

    for i in pullRequests:
        resp = client.get_pull_request(
            pullRequestId=i
        )
        pr = resp['pullRequest']

        link = 'https://{}.console.aws.amazon.com/codesuite/'.format(region) + \
               'codecommit/repositories/{}/pull-requests/'.format(repositoryName) + \
               '{}?region={}'.format(i, region)

        pr['title'] = '<a href="{}" rel="noopener noreferrer" target="_blank">{}</a>'.format(link, pr['title'])

        all_prs.append(pr)

    df = pd.DataFrame(all_prs)

    return df.to_html(escape=False).replace('<th>','<th style = "background-color: gray">')


if __name__ == '__main__':
    client = boto3.client('codecommit')
    region = client.meta.region_name
    port = 8000  # the custom port you want
    app.run(host='127.0.0.1', port=port)
