from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from growth_insights.spiders.growth_details import GrowthSpider
from news_api import fetch_news
from decouple import config

NEWS_API_KEY = config("NEWS_API_KEY")

def get_growth_insights_and_news(crunchbase_url, company_name):

    start_url = crunchbase_url + '/signals_and_news'
    keyword = company_name
    category = 'business,technology,top,science,other'

    settings = get_project_settings()
    process = CrawlerProcess(settings)

    results = []

    def spider_closing(spider):
        nonlocal results
        results = spider.items

    process.crawl(GrowthSpider, url=start_url, spider_closing_callback=spider_closing)
    process.start()

    if not results:
        print("No growth insights data fetched")
        return {}

    news_data = fetch_news(NEWS_API_KEY, keyword, category)
    if not news_data:
        print("No news data fetched")
        return {}

    print(f"Fetched {len(news_data)} news articles")
    top_5_titles = [article['title'] for article in news_data[:5]]
    top_5_titles_str = ', '.join(top_5_titles)
    print(f"Top 5 news titles: {top_5_titles_str}")

    combined_data = {
        'growth_insights': results[0].get('growth insights', '') if results else '',
        'news_articles': top_5_titles_str
    }

    return combined_data

if __name__ == '__main__':
    crunchbase_url = 'https://www.crunchbase.com/organization/zomato'
    company_name = 'zomato'
    result = get_growth_insights_and_news(crunchbase_url, company_name)
    # print(result)
