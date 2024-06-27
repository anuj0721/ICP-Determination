import scrapy

class GrowthSpider(scrapy.Spider):
    name = 'growth_spider'

    def __init__(self, *args, **kwargs):
        super(GrowthSpider, self).__init__(*args, **kwargs)
        self.items = []
        self.spider_closing_callback = kwargs.pop('spider_closing_callback', None)

    def start_requests(self):
        url = getattr(self, 'url', None)
        if url:
            yield scrapy.Request(url=url, callback=self.parse)
        else:
            self.log("Please provide a start URL with -a url='https://www.crunchbase.com/organization/your_organization_name'")

    def parse(self, response):
        data = response.xpath('/html/body/chrome/div/mat-sidenav-container/mat-sidenav-content/div/ng-component/entity-v2/page-layout/div/div/mat-tab-nav-panel/div/full-profile/page-centered-layout/div/div/div[1]/row-card[1]/profile-section/section-card/mat-card/div[2]/phrase-list-card/obfuscation/ai-generated-content/markup-block/field-formatter[1]/blob-formatter/span').get()
        
        item = {
            'growth insights': data
        }
        self.items.append(item)
        return item

    def closed(self, reason):
        if self.spider_closing_callback:
            self.spider_closing_callback(self)
