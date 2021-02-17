import re

import scrapy

from scrapy.loader import ItemLoader
from ..items import OhmanItem
from itemloaders.processors import TakeFirst


class OhmanSpider(scrapy.Spider):
	name = 'ohman'
	start_urls = ['https://www.ohman.lu/om-oss/nyheter/']

	def parse(self, response):
		post_links = response.xpath('//h2/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//div[@class="col-md-10 col-md-push-1 col-lg-8 col-lg-push-2 regular-content"]/h1/text()').get()
		description = response.xpath('//div[@class="post-typography"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="col-md-10 col-md-push-1 col-lg-8 col-lg-push-2 regular-content"]/p[@class="meta"]/text()').get()
		date = date.split('&')[0]

		item = ItemLoader(item=OhmanItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
