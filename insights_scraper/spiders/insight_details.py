import scrapy

class InsightSpider(scrapy.Spider):
    name = 'insight_spider'

    def __init__(self, *args, **kwargs):
        # Initialize the spider and setup data storage and callback
        super(InsightSpider, self).__init__(*args, **kwargs)
        self.items = {
            'growth_insights': '',
            'investment_insights': '',
            'news_insights': ''
        }
        # Optional callback to handle data when the spider closes
        self.spider_closing_callback = kwargs.pop('spider_closing_callback', None)

    def start_requests(self):
        # Start crawling from the provided URL, log an error if not provided
        url = getattr(self, 'url', None)
        if url:
            yield scrapy.Request(url=url, callback=self.parse)
        else:
            self.log("Please provide a start URL with -a url='https://www.crunchbase.com/organization/your_organization_name'")

    def parse(self, response):
        # XPaths for extracting data and their respective titles
        # h2_xpath is xpath has the title of that insight and data_xpath stores the description of that insight
        
        xpaths = [
            {
                'data_xpath': '/html/body/chrome/div/mat-sidenav-container/mat-sidenav-content/div/ng-component/entity-v2/page-layout/div/div/mat-tab-nav-panel/div/full-profile/page-centered-layout/div/div/div[1]/row-card[1]/profile-section/section-card/mat-card/div[2]/phrase-list-card/obfuscation/ai-generated-content/markup-block/field-formatter[1]/blob-formatter/span',
                'h2_xpath': '/html/body/chrome/div/mat-sidenav-container/mat-sidenav-content/div/ng-component/entity-v2/page-layout/div/div/mat-tab-nav-panel/div/full-profile/page-centered-layout/div/div/div[1]/row-card[1]/profile-section/section-card/mat-card/div[1]/div[1]/div/h2'
            },
            {
                'data_xpath': '/html/body/chrome/div/mat-sidenav-container/mat-sidenav-content/div/ng-component/entity-v2/page-layout/div/div/mat-tab-nav-panel/div/full-profile/page-centered-layout/div/div/div[1]/row-card[2]/profile-section/section-card/mat-card/div[2]/phrase-list-card/obfuscation/ai-generated-content/markup-block/field-formatter[1]/blob-formatter/span',
                'h2_xpath': '/html/body/chrome/div/mat-sidenav-container/mat-sidenav-content/div/ng-component/entity-v2/page-layout/div/div/mat-tab-nav-panel/div/full-profile/page-centered-layout/div/div/div[1]/row-card[2]/profile-section/section-card/mat-card/div[1]/div[1]/div/h2'
            },
            {
                'data_xpath': '/html/body/chrome/div/mat-sidenav-container/mat-sidenav-content/div/ng-component/entity-v2/page-layout/div/div/mat-tab-nav-panel/div/full-profile/page-centered-layout/div/div/div[1]/row-card[3]/profile-section/section-card/mat-card/div[2]/phrase-list-card/obfuscation/ai-generated-content/markup-block/field-formatter[1]/blob-formatter/span',
                'h2_xpath': '/html/body/chrome/div/mat-sidenav-container/mat-sidenav-content/div/ng-component/entity-v2/page-layout/div/div/mat-tab-nav-panel/div/full-profile/page-centered-layout/div/div/div[1]/row-card[3]/profile-section/section-card/mat-card/div[1]/div[1]/div/h2'
            }
        ]

        # Extract data and categorize based on their title and stores it into the dictionary
        for xpath_pair in xpaths:
            h2_tag = response.xpath(xpath_pair['h2_xpath'] + '/text()').get()
            data = response.xpath(xpath_pair['data_xpath']).get()
            if h2_tag and data:
                if 'Growth Insight Details' in h2_tag:
                    self.items['growth_insights'] = data
                elif 'Investor Insight Details' in h2_tag:
                    self.items['investment_insights'] = data
                elif 'News Insight Details' in h2_tag:
                    self.items['news_insights'] = data

        yield self.items

    def closed(self, reason):
        # Call the callback function if provided when the spider closes
        if self.spider_closing_callback:
            self.spider_closing_callback(self.items)
