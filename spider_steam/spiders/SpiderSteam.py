import scrapy
from spider_steam.items import SpiderSteamItem


queries = ["arcade", "adventures", "space"]


class SteamSpider(scrapy.Spider):
    name = 'steamspider'
    allowed_domains = ['store.steampowered.com']
    start_urls = ['https://store.steampowered.com/search/?term=']

    def start_requests(self):
        for query in queries:
            cur_url = self.start_urls[0] + query
            yield scrapy.Request(url=cur_url, callback=self.parse_response)


    def parse_response(self, response):
        all_links = response.xpath('//@href').extract()
        for link in all_links:
            if len(link) >= 34 and link[:34] == 'https://store.steampowered.com/app':
                yield scrapy.Request(url=link, callback=self.parse_game)


    def parse_game(self, response):
        item = SpiderSteamItem()
        item['name'] = response.css('div.apphub_AppName::text').get()
        item['category'] = response.xpath('//div[@class="blockbg"]//text()').extract()[1::2][1:-1]
        item['reviews_num'] = response.css('meta[itemprop="reviewCount"]').attrib['content']
        item['review'] = response.xpath('//div[@class="summary column"]//span[@class="game_review_summary positive"]//text()').extract()[0]
        item['release_date'] = response.css('div.date::text').get()
        item['developer'] = response.xpath('//div[@id="developers_list"]//text()').extract()[1]
        tags = response.xpath('//a[@class="app_tag"]//text()').extract()
        for i in range(len(tags)):
            tags[i] = tags[i].strip()
        item['tags'] = tags
        item['price'] = response.xpath('//div[@class="discount_original_price"]//text()').extract()[0]
        platforms = response.xpath('//div[@class="sysreq_tabs"]//text()').extract()
        for i in range(len(platforms)):
            platforms[i] = platforms[i].strip()
        platforms = [x for x in platforms if x != '']
        item['platforms'] = platforms
        yield item
