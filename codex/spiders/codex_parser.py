import scrapy

class CodexParserSpider(scrapy.Spider):
    name = "codex_parser"
    allowed_domains = ["rulaws.ru"]
    start_urls = ["https://rulaws.ru/kodex/"]

    def parse(self, response):
        for item in response.xpath('//div[h2/text()="Популярные материалы" and @class="sidebar-top vgrupe"]/preceding::p[@class="tab-item-title"]'):
            yield {
                'title': item.css('a::attr(title)').get(),
                'href': item.css('a::attr(href)').get()
            }
