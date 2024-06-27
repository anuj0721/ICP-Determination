from itemadapter import ItemAdapter
from bs4 import BeautifulSoup

class CleanHTMLPipeline:
    # Pipeline to clean HTML content and convert it to plain text before storing

    def process_item(self, item, spider):
        """
        Processes each item by cleaning the HTML content in the specified fields.
        Args:
            item (dict): The scraped item with potential HTML content.
            spider (scrapy.Spider): The spider that scraped the item.

        Returns:
            dict: The item with cleaned HTML content.
        """
        item['growth_insights'] = self.clean_html(item.get('growth_insights', ''))
        item['investment_insights'] = self.clean_html(item.get('investment_insights', ''))
        item['news_insights'] = self.clean_html(item.get('news_insights', ''))
        return item

    def clean_html(self, raw_html):
        """
        Cleans the raw HTML content and converts it to plain text.
        Args:
            raw_html (str): The raw HTML content to be cleaned.

        Returns:
            str: The cleaned plain text content.
        """
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(raw_html, 'html.parser')
        # Extract text, joining multiple segments with a space, and strip leading/trailing whitespace
        return soup.get_text(separator=' ').strip()

