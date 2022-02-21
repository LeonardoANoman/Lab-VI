import pandas as pd
import requests

token = input("Entre com seu token: ")

headers = {"Authorization": f"Bearer {token}"}


def run_query(query):
    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

query = """{
  search(query: "stars:>100", type: REPOSITORY, first: 40) {
    nodes {
      ... on Repository {
          total: issues {
          totalCount
        }
        closed: issues(states: CLOSED) {
          totalCount
        }
      }
    }
  }
}"""

result = run_query(query)
results= result["data"]["search"]["nodes"]
data = []

def save_file():
  for r in results:
    closed_issues = r["closed"]["totalCount"]
    total_issues = r["total"]["totalCount"]
    data.append([closed_issues, total_issues])

  columns = ["Closed Issues", "Total Issues"]
  df = pd.DataFrame(data, columns=columns) 
  df.to_excel("issues.xlsx")

save_file()
