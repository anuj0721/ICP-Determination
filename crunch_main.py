from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from insights_scraper.spiders.insight_details import InsightSpider
from news_api import fetch_news
import time

def get_growth_insights_and_news(crunchbase_url, company_name, status, closing_date):
    # Setup the start URL and news API parameters
    start_url = crunchbase_url + '/signals_and_news'
    keyword = company_name
    status = status.lower()
    date = closing_date

    # Get Scrapy project settings
    settings = get_project_settings()

    results = []

    # Define the callback function to handle spider results
    def spider_closing(spider_items):
        nonlocal results
        results.append(spider_items)

    max_retries = 3
    retry_delay = 5  # Seconds between retries
    attempt = 0

    try:
    # Retry mechanism for crawling
        while attempt < max_retries:
            process = CrawlerProcess(settings)
            process.crawl(InsightSpider, url=start_url, spider_closing_callback=spider_closing)
            process.start()

            if results and results[0]:
                break  # Exit the loop if data is fetched

            print(f"Attempt {attempt + 1} failed. Retrying after {retry_delay} seconds...")
            results.clear()
            attempt += 1
            time.sleep(retry_delay)

        if not results or not results[0]:
            print("No growth insights data fetched after retries")
    except Exception as e:
        print(e)


    # Fetch news data using the news API
    # news_data = fetch_news(keyword, status, date)
    # if not news_data:
    #     print("No news data fetched")
    #     news_data = []  # Set news_data to an empty list if no data fetched

    # print(f"Fetched {len(news_data)} news articles")
    # top_10_articles = [{'title': article['title'], 'description': article['description']} for article in news_data[:10]]
    # print(f"Top 10 news articles: {top_10_articles}")

    # Combine insights data with news data
    combined_data = {}
    if results and len(results) > 0:
        combined_data = results[0]
    
    # combined_data.update({"news_articles": top_10_articles})

    return combined_data

if __name__ == '__main__':
    # Main execution with predefined crunchbase URL and company name
    crunchbase_url = 'https://www.crunchbase.com/organization/zomato'  # Input for Crunchbase
    company_name = 'zomato'
    status = 'in progress'
    closing_date = '16/01/2023'  # dd-mm-yyyy
    result = get_growth_insights_and_news(crunchbase_url, company_name, status, closing_date)
    print(result)
