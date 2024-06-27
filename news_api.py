import requests
from datetime import datetime, timedelta
from decouple import config

NEWS_API_KEY = config("NEWS_API_KEY")

def fetch_news(keyword, status, date):
    category = 'business,technology,top,science,other'
    
    if status == 'won':
        to_date = datetime.strptime(date, '%d/%m/%Y')
        
        if to_date < datetime.now() - timedelta(days=365):   # if the given date is earlier than 1 year from the current date
            to_date = datetime.now() - timedelta(days=183)   # fetching news of 6 months to 1 year from the current date
            from_date = datetime.now() - timedelta(days=365)
        else:
            from_date = to_date - timedelta(days=183)  # Six months before the given date
            if from_date < datetime.now() - timedelta(days=365): # if from_date goes before 1 year fetching news up to 1 year from current date
                from_date = datetime.now() - timedelta(days=365)
    else:
        to_date = datetime.now()
        from_date = to_date - timedelta(days=183)  # Six months before today
    
    from_date_str = from_date.strftime('%Y-%m-%d')
    to_date_str = to_date.strftime('%Y-%m-%d')
    
    print(f"Fetching news from {from_date_str} to {to_date_str}")
    
    url = f"https://newsdata.io/api/1/archive?apikey={NEWS_API_KEY}&qInTitle={keyword}&language=en&from_date={from_date_str}&to_date={to_date_str}&category={category}"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("results", [])
    else:
        print(f"Error retrieving data: {response.status_code}, Response: {response.text}")
        return []


