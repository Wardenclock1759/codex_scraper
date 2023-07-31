import scrapy
import json
from urllib.parse import urlparse
from scrapy import signals
from pydispatch import dispatcher

class CodexCollectorSpider(scrapy.Spider):
    name = "codex_collector"
    allowed_domains = ["rulaws.ru"]
    custom_settings = {
         'CONCURRENT_REQUESTS' : 1
    }

    def __init__(self, *args, **kwargs):
        super(CodexCollectorSpider, self).__init__(*args, **kwargs)
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def start_requests(self):
        base_url = "https://rulaws.ru/"

        with open('urls.json', 'r') as f:
            self.data = json.load(f)

        self.tree = {}
        for item in self.data:
            url = base_url + item['href'].lstrip('/')
            request = scrapy.Request(url=url, callback=self.parse)
            request.meta['node'] = self.tree
            yield request

    def parse(self, response):
        breadcrumbs = []
        codex_title = response.css('section.content .sidebar-top.vgrupe h1::text').get()
        codex_title = codex_title.replace('\n', '').replace('\t', '')
        self.codex_title = codex_title

        self.tree[codex_title] = {}
        breadcrumbs.append(self.tree[codex_title])

        for row in response.css('tr'):
            div = row.css('div')[0]
            depth = int(div.css('::attr(class)').re_first('marg(\d+)')) if div.css('::attr(class)').re_first('marg(\d+)') else 0
            title = div.css('a::text').get() or div.css('::text').get()
            title = title.replace('\n', '').replace('\t', '')
            
            node = {}
            breadcrumbs[depth][title] = node

            if "t-statya" in div.css('::attr(class)').get():
                base_url = "https://rulaws.ru"
                article_url = div.css('a::attr(href)').get()
                url = base_url + article_url
                yield scrapy.Request(url=url, callback=self.parse_article, meta={'node': node})
            else:
                breadcrumbs = breadcrumbs[:depth + 1] + [node]

    def parse_article(self, response):
        node = response.meta['node']

        content_div = response.css('div[itemprop="text"]')

        if content_div.css('div.comment-source'):
            content_p = content_div.xpath('.//p[following-sibling::div[contains(@class, "comment-source")]]/text()').getall()
            comment_p = content_div.css('div.comment-source ~ p:not([class])::text').getall()
        else:
            content_p = content_div.css('p:not([class])::text').getall()
            comment_p = []

        content = ' '.join(content_p).replace('\n', '').replace('\t', '')

        node["Текст статьи"] = content
        node["Текст комментариев"] = comment_p

    def spider_closed(self, spider):
        filename = self.codex_title.replace(' ', '_') + '.json'
        with open(filename, 'w', encoding='utf8') as f:
            json.dump(self.tree, f, ensure_ascii=False)