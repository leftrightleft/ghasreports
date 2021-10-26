import os
import json

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
    
f = open("demofile2.txt", "a")
for repo in repos:
  res = requests.get(f'https://api.github.com/repos/{org}/{repo}/code-scanning/alerts', headers=header)
  if len(json.dumps(res.json())) > 1:
    f.write(json.dumps(res.json(), indent=2))
    f.write("\n")
f.close()
