This Python script uses the new `search/jql` [endpoint](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-search/#api-rest-api-3-search-jql-get) from the Jira Cloud REST API (v3) to fetch issues from your instance using a JQL query, then exports the results to a CSV file. In the script we are handling pagination, making it ideal for large datasets.

### Requirements

- Python 3.x
- `pandas`
- `requests`

You can install the required packages with:

```bash
pip install pandas requests
```

### Usage 

```bash
python main.py
```

### Example output

| key    | id    | summary              | description          |
| ------ | ----- | -------------------- | -------------------- |
| TEST-1 | 10001 | Fix login issue      | User cannot login... |
| TEST-2 | 10002 | Update documentation | Added usage examples |


