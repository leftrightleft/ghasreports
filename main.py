import os
import json
import requests
import csv

org = 'octodemo'
header = {'Authorization': 'token ' + os.environ['TOKEN']}

repos = []
res = requests.get(f'https://api.github.com/orgs/{org}/repos?type=all', headers=header)
for repo in res.json():
  repos.append(repo['name'])

# This code handles paging. docs: https://developer.github.com/v3/guides/traversing-with-pagination/
# while 'next' in res.links.keys():
#   res=requests.get(res.links['next']['url'],headers=header)
#   for repo in res.json():
#     repos.append(repo['name'])
    
results = []
for repo in repos:
  res = requests.get(f'https://api.github.com/repos/{org}/{repo}/code-scanning/alerts', headers=header)
  if isinstance(res.json(), list):
    results.append({repo:res.json()})
    
with open('vulnerabilities.csv', 'w', newline='') as csvfile:
    vulnwriter = csv.writer(csvfile, delimiter=',')
    vulnwriter.writerow(['repo', 'number', 'created at', 'state', 'url', 'rule id', 'severity level', 'tool name', 'path'])
    for result in results:
        print(result)
        for k, v in result.items():
            for value in v:
                vulnwriter.writerow([k,
                                    value['number'],
                                    value['created_at'],
                                    value['state'],
                                    value['html_url'],
                                    value['rule']["id"],
                                    value['rule'].get("security_severity_level", 'n/a'),
                                    value['tool']['name'],
                                    value['most_recent_instance']['location']['path']
                                    ])
