import scrapy
from selenium import webdriver

class HotelSpider(scrapy.Spider):
    name = "hotel_crawler"
    allowed_domains = ['booking.com']
    
    start_urls = ['https://www.booking.com/hotel/ph/red-planet-manila-bay-manila.en-gb.html?aid=304142;label=gen173nr-1FCAEoggJCAlhYSDNYBGi0AYgBAZgBLsIBCndpbmRvd3MgMTDIAQ_YAQHoAQH4AQuSAgF5qAID;sid=d1cefe2b1ccb1dd74325d599983f140c;all_sr_blocks=266128901_105636671_2_0_0;checkin=2018-06-13;checkout=2018-06-14;dest_id=-2437894;dest_type=city;dist=0;group_adults=2;hapos=1;highlighted_blocks=266128901_105636671_2_0_0;hpos=1;room1=A;sb_price_type=total;srepoch=1528865568;srfid=240de3bab9026fe7fa53e68e5358b24fe5f4d157X1;srpvid=63e5224fd68c002c;type=total;ucfs=1&#hotelTmpl']

    def parse(self, response):
        yield {
                'hotel_name': response.xpath('.//h2[@id="hp_hotel_name"]/text()').extract_first()
        }
