# -*- coding: utf-8 -*-
import scrapy


class SpecialOffersSpider(scrapy.Spider):
    name = 'special_offers'
    allowed_domains = ['web.archive.org']
    def start_requests(self):
        yield scrapy.Request(url='https://web.archive.org/web/20190225123327/https://www.tinydeal.com/specials.html', callback=self.parse, headers = {
  'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'
})
    def parse(self, response):
        products = response.xpath("//ul[@class='productlisting-ul']/div/li")
        for product in products:
            yield {
                'title':product.xpath('.//a[@class="p_box_title"]/text()').get(),
                'url':  response.urljoin(product.xpath('.//a[@class="p_box_title"]/@href').get()),
                'discounted_price':product.xpath('.//span[@class="productSpecialPrice fl"]/text()').get(),
                'original_price': product.xpath('.//span[@class="normalprice fl"]/text()').get(),
                'user-agent': str(response.request.headers['User-Agent'])
            }
        next_page = response.xpath("//a[@class='nextPage']/@href").get()
        if next_page:
            yield response.follow(url=next_page, callback=self.parse, headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'})

