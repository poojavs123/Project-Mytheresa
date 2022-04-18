import scrapy
from mytheresashoes.items import *
from scrapy.http import Request

class MytheresaSpider (scrapy.Spider):
    name = "mytheresashoes"

    start_urls = [
        'https://www.mytheresa.com/int_en/men/shoes.html'
    ]

    def parse(self, response):
        product_url = response.xpath('//div[@class="category-products"]/ul/li[starts-with(@class,item)]/a[1]/@href').extract()

        for products in product_url:
            yield Request(url=products, callback=self.parse_data)

        next_page = response.xpath('//li[@class="next"]/a/@href').extract_first()

        if next_page is not None:
            next_page_link = response.urljoin(next_page)
            yield scrapy.Request(url= next_page_link, callback= self.parse)


    def parse_data(self,response):
        breadcrumbs = response.xpath('//li[starts-with(@class, "category")]/a/span/text()').extract()

        image = response.xpath('//*[@id="image-0"]/@src').extract_first()
        image_url = "http:" + str(image)

        brand = response.xpath('//div[@class="product-designer"]/span/a/text()').extract_first()

        product_name = response.xpath('//div[@class="product-name"]/span/text()').extract_first()

        listing_price = response.xpath('//div[contains(@class,"price-info")]/div/p[@class="old-price"]/span/text()').extract_first()

        offer_price = response.xpath('//div[contains(@class,"price-info")]/div/p[@class="special-price"]/span/text()').extract_first()

        discount = response.xpath('//div[contains(@class,"price-info")]/span/text()').extract_first()

        product_id = response.xpath('//div[@class="product-shop"]/div[@class="product-sku pa1-rm-tax"]/span[@class="h1"]/text()').extract_first()[9::]

        sizes = response.xpath('//ul[@class="sizes"]/li/a[contains(text(),"EU")]/text()|//ul[@class="sizes"]/li/a/span[contains(text(),"EU")]/text()').extract()

        description = response.xpath('//div[@class="product-collateral toggle-content accordion-open"]//dl//dd//div//p[@class="pa1-rmm product-description"]/text()|//div[@class="product-collateral toggle-content accordion-open"]//dl//dd//div//ul[@class="disc featurepoints"]/li/text()').extract()

        other_images_link = response.xpath('//div[@class="more-views"]//ul//li//img/@src').extract()
        other_images = []
        for images in other_images_link:
            image_url = "http:"+ images
            other_images.append(image_url)

        item = mytheresashoes(
            breadcrumbs = breadcrumbs,
            image_url = image_url,
            brand = brand,
            product_name = product_name,
            listing_price = listing_price,
            offer_price = offer_price,
            discount = discount,
            product_id = product_id,
            sizes = sizes,
            description = str(description),
            other_images = other_images,
        )
        yield item

