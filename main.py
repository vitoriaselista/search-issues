import os
import pandas as pd
import requests

# Jira Admin credentials
base_url = 'https://your-instance.atlassian.net/'
email = 'your-email'
api_key = 'your-api-key'
auth = (email, api_key)

headers = {
    "Content-Type": "application/json"
}

def get(url, params={}):
    return requests.get(url, params=params, auth=auth, headers=headers)

def search(jql):
    issues = []
    nextPageToken = None
    maxResults = 1000  # max 5000

    while True:
        params = {
            "jql": jql,
            "maxResults": maxResults,
            "fields": "summary,description",  # Customize with your fields
            "expand": "names",
            "fieldsByKeys": True,
            "failFast": False
        }

        if nextPageToken:
            params["nextPageToken"] = nextPageToken

        response = get(f"{base_url}/rest/api/3/search/jql", params=params)

        if response.status_code != 200:
            print("Error:", response.status_code, response.text)
            break

        results = response.json()
        batch = []

        for i in results.get('issues', []):
            batch.append({
                'key': i['key'],
                'id': i['id'],
                'summary': i['fields'].get('summary', ''),
                'description': i['fields'].get('description', '')
            })

        issues += batch

        # Checks if there is a next page of isues
        nextPageToken = results.get('nextPageToken')
        if not nextPageToken:
            break

    return issues

# Run the search using a bounded JQL query
jql = "your-jql-ordened"
issues = search(jql)

# Export to csv
pd.DataFrame(issues).to_csv('search-issues.csv', index=False)
print(f"{len(issues)} successfully exported.")
