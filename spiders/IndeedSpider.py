import scrapy

class IndeedSpider(scrapy.Spider):
	name = "Indeed"
	allowed_domains = ["indeed.com"]
	start_urls = ["http://www.indeed.com/cmp/Goldman-Sachs/reviews"]

	def parse(self, response):
		print(response.body)
		reviews = response.xpath("//div[@class = 'cmp-review']")
		for review in reviews:
			rating = review.xpath("/div[@class = 'cmp-review-heading']/text()").extract()
			title = review.xpath("/div[@class = 'cmp-review-title']/span[@itemprop = 'name']/text()").extract()
			print(rating)
			print(title)


