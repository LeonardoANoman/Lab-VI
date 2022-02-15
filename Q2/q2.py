import requests
import json
import pandas as pd
import key as key

query = """query {
  search(query: "stars:>1", type: REPOSITORY, first: 100) {
    nodes {
      ... on Repository {
        mergedPullRequests: pullRequests(states: MERGED) {
          totalCount
        }
      }
    }
  }
}"""

url = 'https://api.github.com/graphql'
headers = {"Authorization": "Bearer " + key.AUTH_TOKEN}
r = requests.post(url, headers=headers,json={'query': query})

# print(r.text) 

json_data = json.loads(r.text)

df_data = json_data['data']['search']['nodes']
df = pd.DataFrame(df_data)
df.to_excel("Q2/q2.xlsx")
