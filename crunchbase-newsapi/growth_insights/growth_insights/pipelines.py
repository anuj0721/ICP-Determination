from itemadapter import ItemAdapter
from bs4 import BeautifulSoup

class CleanHTMLPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        for field in adapter.keys():
            if isinstance(adapter[field], str):
                soup = BeautifulSoup(adapter[field], 'html.parser')
                adapter[field] = soup.get_text(separator=' ')
        return item
