
import requests
from datetime import datetime
from datetime import date

headers = {"Authorization": "Bearer otokenvaiaquitem40caractereseuconteiiiii"}


def run_query(query):
    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

query = """query{
  search(query: "stars:>100", type: REPOSITORY, first: 100) {
    nodes {
      ... on Repository {
        nameWithOwner
        url
        createdAt
        releases{
          totalCount
        }
        primaryLanguage {
          name
        }

      }
    }
  }
}"""

result = run_query(query)
results= result["data"]["search"]["nodes"]

def save_file():
  for r in results:
    name = r["nameWithOwner"]
    today = date.today()
    created_at = date.fromisoformat(r["createdAt"][0:10])
    age = (today - created_at).days # Calcula diferença de dias da criação do repositório
    total_releases = r["releases"]["totalCount"]
    primary_language = "" if r["primaryLanguage"] is None else r["primaryLanguage"]["name"]
    print(name , age , total_releases,primary_language) # salvar esses dados, na   ordem  das perguntas no arquivo csv


save_file()
