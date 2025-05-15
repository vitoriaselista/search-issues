import os
import pandas as pd
import requests

# Jira Admin credentials
email = "your-email"
api_key = "your-api-key"
base_url = "https://your-instance.atlassian.net"
auth = (email, api_key) # Basic authentication

# request headers for Jira REST API
headers = {
    "Content-Type": "application/json"
}

# Helper function to perform GET requests with auth and headers
def get(url, params={}):
    return requests.get(url, params=params, auth=auth, headers=headers)

# Function to search for Jira issues using JQL and pagination
def search(jql):
    issues = [] # Will hold all fetched issues
    startAt = 0 # Pagination start index
    maxResults = 5000   # Maximum number of results per request (Jira Cloud new limit)

    while True:
        # Request issues
        response = get(
            f"{base_url}/rest/api/3/search/jql",
            params={
                "jql": jql,
                "startAt": startAt,
                "maxResults": maxResults,
                "fields": "*all"
            }
        )

        results = response.json()

        # Process current batch of issues
        batch = []
        for i in results.get('issues', []):
            key = i['key']
            summary = i['fields'].get('summary')
            description = i['fields'].get('description', '')

            # here we add all data to a dictionary to be transformed into a csv
            treated = {
                'key': key,
                'id': i['id'],
                'summary': summary,
                'description': description
            }
            batch.append(treated)

        issues += batch

        # Stop if all issues have been retrieved
        if startAt + maxResults >= results.get('total', 0):
            break
        else:
            # Move to next page
            startAt += maxResults

    return issues

# Run the search using a JQL query
jql = "your jql here"
issues = search(jql)

# Export results to a CSV file
pd.DataFrame(issues).to_csv('search-issues.csv', index=False)

# Print confirmation message
print(f"{len(issues)} successfully exported.")
