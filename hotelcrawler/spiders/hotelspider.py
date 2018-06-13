import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class HotelSpider(scrapy.Spider):
    name = "hotel_crawler"
    allowed_domains = ['booking.com']
    
    start_urls = ['https://www.booking.com/hotel/ph/red-planet-manila-bay-manila.en-gb.html?aid=304142;label=gen173nr-1FCAEoggJCAlhYSDNYBGi0AYgBAZgBLsIBCndpbmRvd3MgMTDIAQ_YAQHoAQH4AQuSAgF5qAID;sid=d1cefe2b1ccb1dd74325d599983f140c;all_sr_blocks=266128901_105636671_2_0_0;checkin=2018-09-13;checkout=2018-09-14;dest_id=-2437894;dest_type=city;dist=0;group_adults=1;group_children=0;hapos=1;highlighted_blocks=266128901_105636671_2_0_0;hpos=1;no_rooms=1;room1=A;sb_price_type=total;srepoch=1528865568;srfid=240de3bab9026fe7fa53e68e5358b24fe5f4d157X1;srpvid=63e5224fd68c002c;type=total;ucfs=1&#hotelTmpl']
    #start_urls = ['https://www.booking.com/searchresults.en-gb.html?label=gen173nr-1FCAQoggJCC3JlZ2lvbl81MjU4SAlYBGi0AYgBAZgBLsIBCndpbmRvd3MgMTDIAQ_YAQHoAQH4AQKSAgF5qAID&sid=d42d69c201c210da5ba401e54684cb03&sb=1&src=searchresults&src_elem=sb&error_url=https%3A%2F%2Fwww.booking.com%2Fsearchresults.en-gb.html%3Flabel%3Dgen173nr-1FCAQoggJCC3JlZ2lvbl81MjU4SAlYBGi0AYgBAZgBLsIBCndpbmRvd3MgMTDIAQ_YAQHoAQH4AQKSAgF5qAID%3Bsid%3Dd42d69c201c210da5ba401e54684cb03%3Bcity%3D-2437894%3Bclass_interval%3D1%3Bdest_id%3D5258%3Bdest_type%3Dregion%3Bdtdisc%3D0%3Binac%3D0%3Bindex_postcard%3D0%3Blabel_click%3Dundef%3Bnflt%3Dclass%253D5%253Bclass%253D4%253Bclass%253D3%253Bclass%253D2%253Bclass%253D1%253B%253Bht_id%253D204%3Boffset%3D0%3Bpostcard%3D0%3Braw_dest_type%3Dregion%3Broom1%3DA%252CA%3Bsb_price_type%3Dtotal%3Bss%3DMetro%2520Manila%252C%2520Philippines%3Bss_all%3D0%3Bssb%3Dempty%3Bsshis%3D0%26%3B&ss=Metro+Manila&ssne=Metro+Manila&ssne_untouched=Metro+Manila&region=5258&checkin_monthday=13&checkin_month=6&checkin_year=2018&checkout_monthday=14&checkout_month=6&checkout_year=2018&group_adults=1&group_children=0&no_rooms=1&from_sf=1']
    def __init__(self):

        chrome_options = Options()
        #chrome_options.add_argument("--headless")
        prefs = {'profile.managed_default_content_settings.images':2}
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(chrome_options=chrome_options)

    def parse(self, response):
        self.driver.get(response.url)

        #'hotel_name': self.driver.find_element_by_xpath('//h2[@id="hp_hotel_name"]').text,
        #       'address': self.driver.find_element_by_xpath('//span[contains(@class, "hp_address_subtitle")]').text,
        yield {
                'hotel_name': response.xpath('normalize-space(//h2[@id="hp_hotel_name"]/text())'),
                'address': response.xpath('normalize-space(//span[contains(@class, "hp_address_subtitle")]/text())').extract_first(),
                'circles': response.xpath('count(//span[contains(@class, "hp__hotel_ratings__stars")]//circle)').extract_first(),
                'rating': response.xpath('normalize-space(//span[contains(@class, "review-score-widget")]/span[contains(@class, "review-score-badge")]/text())').extract_first(),
                'summary': response.xpath('normalize-space(//div[@id="summary"]/span/text())').extract_first(),
                'check-in-date': response.xpath('//a[contains(@class, "av-summary-checkin")]/text()').extract_first(),
                'check-out-date': response.xpath('normalize-space(//a[contains(@class, "av-summary-checkout")]/text())').extract_first(),
                'price': response.xpath('normalize-space(//span[contains(@class, "hprt-price-price-standard")]/text())').extract_first()
        }
