import math
import pandas as pd
import requests
from datetime import datetime
from datetime import date

from sqlalchemy import column


token = input("Entre com seu token: ")

headers = {"Authorization": f"Bearer {token}"}


def run_query(query):
    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

query = """{
  search(query: "stars:>100", type: REPOSITORY, first: 100) {
    nodes {
      ... on Repository {
        nameWithOwner
        url
        createdAt
        releases {
          totalCount
        }
        primaryLanguage {
          name
        }
        mergedPullRequests: pullRequests(states: MERGED) {
          totalCount
        }
        updatedAt
      }
    }
  }
}"""

#  This query is used to get total and closed issues. First 40 so that the API doesn't break.
# 
# query = """{
#   search(query: "stars:>100", type: REPOSITORY, first: 40) {
#     nodes {
#       ... on Repository {
#           total: issues {
#           totalCount
#         }
#         closed: issues(states: CLOSED) {
#           totalCount
#         }
#       }
#     }
#   }
# }"""



result = run_query(query)
results= result["data"]["search"]["nodes"]
data = []

def save_file():
  for r in results:
    name = r["nameWithOwner"]
    today = date.today()
    created_at = date.fromisoformat(r["createdAt"][0:10])
    age = (today - created_at).days # Calcula diferença de dias da criação do repositório
    total_releases = r["releases"]["totalCount"]
    primary_language = "None" if r["primaryLanguage"] is None else r["primaryLanguage"]["name"]
    total_pull_requests = r["mergedPullRequests"]["totalCount"]
    today_minutes = datetime.utcnow()
    updated_at =  datetime.strptime(r["updatedAt"], "%Y-%m-%dT%H:%M:%SZ")
    updated_minutes = today_minutes - updated_at
    updated = math.modf(updated_minutes.seconds / 60)[1]
    # closed_issues = r["closed"]["totalCount"]
    # total_issues = r["total"]["totalCount"]
    data.append([name, age, total_pull_requests, total_releases, updated, primary_language])

  columns = ["Name", "Age", "Total Pull Requests", "Total Releases", "Updated", "Primary Language"]
  df = pd.DataFrame(data, columns=columns) 
  df.to_excel("repositorios_populares.xlsx")

save_file()
