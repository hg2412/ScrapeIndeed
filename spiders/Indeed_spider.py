import scrapy
from ScrapeIndeed.items import ScrapeindeedItem

class IndeedSpider(scrapy.Spider):
	name = "Indeed"
	allowed_domains = ["indeed.com"]
	start_urls = ["http://www.indeed.com/Best-Places-to-Work"]

	def parse(self, response):
		comp_links = response.xpath("//div[@class='cmp-company-tile-name']/a[@itemprop = 'url']/@href").extract()
		comp_links.extend(response.xpath("//span[@class='cmp-company-tile-name']/a[@itemprop = 'url']/@href").extract())
		print(comp_links)
		for comp in comp_links:
			print("Parsing " + comp)
			yield scrapy.Request(response.urljoin(comp) + '/reviews', callback=self.parse_company)


	def parse_company(self, response):
		comp_name = response.url.split('/')[-2]
		print('Company Name:')
		print(comp_name)
		reviews = response.xpath("//div[@class = 'cmp-review-container']/div[@class='cmp-review']")
		for review in reviews:
			rating = review.xpath("div[@class='cmp-review-heading']/div[@class='cmp-ratings']/div[@class='cmp-rating-expandable']/span[@class='cmp-rating-outer']/span[@class='cmp-rating-inner rating']/span[@class='cmp-value-title']").xpath("@title").extract()
			title = review.xpath("div[@class='cmp-review-heading']/div[@class='cmp-review-title']/span/text()").extract()
			comment = review.xpath("*/div[@class='cmp-review-description']/span[@class='cmp-review-text']/text()").extract()

			item = ScrapeindeedItem()
			item['company'] = comp_name
			item['rating'] = rating
			item['title'] = title
			item['comment'] = comment
			yield item

		next_page = response.xpath("//a[@data-tn-element='next-page']/@href").extract()
		if next_page:
			print("Next page is:")
			url = response.urljoin(next_page[0])
			print(url)
			yield scrapy.Request(url, callback=self.parse_company)