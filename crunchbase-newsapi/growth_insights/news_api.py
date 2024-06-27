import requests
from datetime import datetime, timedelta

def fetch_news(api_key, keyword, category):
    from_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    to_date = datetime.now().strftime('%Y-%m-%d')

    url = f"https://newsdata.io/api/1/archive?apikey={api_key}&qInTitle={keyword}&language=en&from_date={from_date}&to_date={to_date}&category={category}"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("results", [])
    else:
        print(f"Error retrieving data: {response.status_code}")
        return []
