import scrapy
from selenium import webdriver

class HotelSpider(scrapy.Spider):
    name = "hotel_crawler"
    allowed_domains = ['booking.com']
    
    start_urls = ['https://www.booking.com/hotel/ph/red-planet-manila-bay-manila.en-gb.html?label=gen173nr-1DCAsotAFCHHJlZC1wbGFuZXQtbWFuaWxhLWJheS1tYW5pbGFICVgEaLQBiAEBmAEuwgEKd2luZG93cyAxMMgBD9gBA-gBAfgBApICAXmoAgM;sid=d1cefe2b1ccb1dd74325d599983f140c;all_sr_blocks=266128901_105636671_2_0_0;checkin=2018-06-13;checkout=2018-06-14;dest_id=-2437894;dest_type=city;dist=0;group_adults=1;group_children=0;hapos=1;highlighted_blocks=266128901_105636671_2_0_0;hpos=1;no_rooms=1;room1=A;sb_price_type=total;srepoch=1528874246;srfid=2b754447bef02f0d6a7c09fe9036dc79166d621bX1;srpvid=274533424960016d;type=total;ucfs=1&#hotelTmpl']

    def __init__(self):
            self.driver = webdriver.Firefox()

    def parse(self, response):
        self.driver.get(response.url)

        yield {
                'hotel_name': self.driver.find_element_by_xpath('//h2[@id="hp_hotel_name"]').text,
                'address': self.driver.find_element_by_xpath('//span[contains(@class, "hp_address_subtitle")]').text,
                'circles': response.xpath('count(//span[contains(@class, "hp__hotel_ratings__stars")]//circle)').extract_first(),
                'rating': response.xpath('normalize-space(//span[contains(@class, "review-score-widget")]/span[contains(@class, "review-score-badge")]/text())').extract_first(),
                'summary': response.xpath('normalize-space(//div[@id="summary"]/span/text())').extract_first(),
                'check-in-date': response.xpath('//a[contains(@class, "av-summary-checkin")]/text()').extract_first(),
                'check-out-date': response.xpath('normalize-space(//a[contains(@class, "av-summary-checkout")]/text())').extract_first(),
                'price': response.xpath('normalize-space(//span[contains(@class, "hprt-price-price-standard")]/text())').extract_first()
        }
