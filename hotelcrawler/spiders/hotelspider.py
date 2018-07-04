import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
import urllib
from urllib.parse import urlencode, parse_qs, urlsplit, urlunsplit
import datetime  
from datetime import timedelta
import unicodedata
import time

class HotelSpider(scrapy.Spider):
    name = "hotel_crawler"
    allowed_domains = ['booking.com']
    
    #start_urls = ['https://www.booking.com/hotel/ph/red-planet-manila-bay-manila.en-gb.html?aid=304142;label=gen173nr-1FCAEoggJCAlhYSDNYBGi0AYgBAZgBLsIBCndpbmRvd3MgMTDIAQ_YAQHoAQH4AQuSAgF5qAID;sid=d1cefe2b1ccb1dd74325d599983f140c;all_sr_blocks=266128901_105636671_2_0_0;checkin=2018-09-13;checkout=2018-09-14;dest_id=-2437894;dest_type=city;dist=0;group_adults=1;group_children=0;hapos=1;highlighted_blocks=266128901_105636671_2_0_0;hpos=1;no_rooms=1;room1=A;sb_price_type=total;srepoch=1528865568;srfid=240de3bab9026fe7fa53e68e5358b24fe5f4d157X1;srpvid=63e5224fd68c002c;type=total;ucfs=1&#hotelTmpl']
    #start_urls = ['https://www.booking.com/searchresults.en-gb.html?label=gen173nr-1FCAQoggJCC3JlZ2lvbl81MjU4SAlYBGi0AYgBAZgBLsIBCndpbmRvd3MgMTDIAQ_YAQHoAQH4AQKSAgF5qAID&sid=d42d69c201c210da5ba401e54684cb03&sb=1&src=searchresults&src_elem=sb&error_url=https%3A%2F%2Fwww.booking.com%2Fsearchresults.en-gb.html%3Flabel%3Dgen173nr-1FCAQoggJCC3JlZ2lvbl81MjU4SAlYBGi0AYgBAZgBLsIBCndpbmRvd3MgMTDIAQ_YAQHoAQH4AQKSAgF5qAID%3Bsid%3Dd42d69c201c210da5ba401e54684cb03%3Bcity%3D-2437894%3Bclass_interval%3D1%3Bdest_id%3D5258%3Bdest_type%3Dregion%3Bdtdisc%3D0%3Binac%3D0%3Bindex_postcard%3D0%3Blabel_click%3Dundef%3Bnflt%3Dclass%253D5%253Bclass%253D4%253Bclass%253D3%253Bclass%253D2%253Bclass%253D1%253B%253Bht_id%253D204%3Boffset%3D0%3Bpostcard%3D0%3Braw_dest_type%3Dregion%3Broom1%3DA%252CA%3Bsb_price_type%3Dtotal%3Bss%3DMetro%2520Manila%252C%2520Philippines%3Bss_all%3D0%3Bssb%3Dempty%3Bsshis%3D0%26%3B&ss=Metro+Manila&ssne=Metro+Manila&ssne_untouched=Metro+Manila&region=5258&checkin_monthday=13&checkin_month=6&checkin_year=2018&checkout_monthday=14&checkout_month=6&checkout_year=2018&group_adults=1&group_children=0&no_rooms=1&from_sf=1']
    #start_urls = ['https://www.booking.com/searchresults.en-gb.html?region=5258;ss=Metro%2BManila']
    #start_urls = ['https://www.booking.com/searchresults.en-gb.html?region=5630;ss=Davao%2C%20Philippines']
    #start_urls = ['https://www.booking.com/hotel/ph/red-planet-binondo.en-gb.html?aid=304142;label=gen173nr-1FCAQoggJCE3NlYXJjaF9tZXRybyttYW5pbGFICVgEaLQBiAEBmAEuwgEKd2luZG93cyAxMMgBDNgBAegBAfgBApICAXmoAgM;sid=78e774a890731222a7398aead8e3d850;all_sr_blocks=266128701_105636643_2_0_0;checkin=2018-06-21;checkout=2018-06-22;dest_id=-2437894;dest_type=city;dist=0;dotd_fb=1;hapos=1;highlighted_blocks=266128701_105636643_2_0_0;hpos=1;nflt=class%3D1%3Bclass%3D2%3Bclass%3D3%3Bclass%3D4%3Bclass%3D5%3Bht_id%3D204;room1=A;sb_price_type=total;srepoch=1528913348;srfid=69eec472f4147f110a73f67557b310b05c8bc005X1;srpvid=f87d7fa1a7f00149;type=total;ucfs=1&#hotelTmpl']
    reqResults = -1
    offset = 0

    def __init__(self, loc='', numhotels=-1, offset=0, *args, **kwargs):
        super(HotelSpider, self).__init__(*args, **kwargs)
        if loc == 'baguio':
            self.start_urls.append('https://www.booking.com/searchresults.en-gb.html?city=-2410361')
        elif loc == 'bohol':
            self.start_urls.append('https://www.booking.com/searchresults.en-gb.html?region=5469')
        elif loc == 'camsur':
            self.start_urls.append('https://www.booking.com/searchresults.en-gb.html?region=6399')
        elif loc == 'cebu':
            self.start_urls.append('https://www.booking.com/searchresults.en-gb.html?region=5374')
        elif loc == 'davao':
            self.start_urls.append('https://www.booking.com/searchresults.en-gb.html?region=5630;ss=Davao%2C%20Philippines')
        elif loc == 'launion':
            self.start_urls.append('https://www.booking.com/searchresults.html?city=-2432442')
        elif loc == 'manila':
            self.start_urls.append('https://www.booking.com/searchresults.en-gb.html?region=5258;ss=Metro%2BManila')
        elif loc == 'palawan':
            self.start_urls.append('https://www.booking.com/searchresults.en-gb.html?region=1505')
        elif loc == 'siargao':
            self.start_urls.append('https://www.booking.com/searchresults.en-gb.html?region=5375')
        elif loc == 'vigan':
            self.start_urls.append('https://www.booking.com/searchresults.en-gb.html?city=-2459765')

        self.reqResults = int(numhotels)
        self.offset = int(offset)
        chrome_options = Options()
       # chrome_options.add_argument("--headless")
       # chrome_options.add_argument("--window-size=1400x900")
        prefs = {'profile.managed_default_content_settings.images':2}
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_path = "driver/chromedriver"
        self.driver = webdriver.Chrome(executable_path=chrome_path, chrome_options=chrome_options)

    def parse(self, response):
        self.driver.get(response.url)

        time.sleep(1)
        #self.driver.find_element_by_xpath('//td[contains(@class, "c2-day-s-today")]').click()

        selectNumber = Select(self.driver.find_element_by_xpath('//select[@name="group_adults"]'))
        selectNumber.select_by_value("1")

        self.driver.find_element_by_xpath('//button[contains(@class, "sb-searchbox__button")]').click()

        self.driver.get(self.driver.current_url + "&no_dorms=1")

        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "1 star")]')))

        elem = self.driver.find_elements_by_xpath('//span[contains(text(), "1 star")]')
        if len(elem) > 0:
            elem[0].click()
        time.sleep(1)
        elem = self.driver.find_elements_by_xpath('//span[contains(text(), "2 star")]')
        if len(elem) > 0:
            elem[0].click()
        time.sleep(1)
        elem = self.driver.find_elements_by_xpath('//span[contains(text(), "3 star")]')
        if len(elem) > 0:
            elem[0].click()
        time.sleep(1)
        elem = self.driver.find_elements_by_xpath('//span[contains(text(), "4 star")]')
        if len(elem) > 0:
            elem[0].click()
        time.sleep(1)
        elem = self.driver.find_elements_by_xpath('//span[contains(text(), "5 star")]')
        if len(elem) > 0:
            elem[0].click()
        time.sleep(1)
        self.driver.find_element_by_xpath('//div[contains(@class, "filter_item")]/span[contains(text(), "Hotels")]').click()
        time.sleep(1)
        #self.driver.find_element_by_xpath('//li[contains(@class, "sort_distance_from_landmark")]/a').click()
        elem = self.driver.find_elements_by_xpath('//li[contains(@class, "sort_bayesian_review_score")]/a')
        if len(elem) > 0:
            elem[0].click()
        time.sleep(3)
        #search_results_source = self.driver.page_source
        #sr_selector = Selector(text=search_results_source.encode('utf-8'))
        #results_list = sr_selector.xpath('//div[contains(@class, "sr_item_content")]')

        hotels_list = {}
        resultsParsed = 0
        
        #self.reqResults = -1
        #self.reqResults = 2
        stopParse = False

        while self.reqResults == -1 or resultsParsed < self.reqResults + self.offset:
            ##for each results page, get the result items
            results_list = self.driver.find_elements_by_xpath('//div[contains(@class, "sr_item_content")]')

            ##for each result item, add them to url dictionary
            for result in results_list:
                url = result.find_element_by_xpath('.//a[contains(@class, "hotel_name_link")]').get_attribute("href")
                try:
                    location_from_center = result.find_element_by_xpath('.//span[contains(@class, "distfromdest_clean")]').text
                    #location_from_center = unicodedata.normalize("NFKD", result.xpath('normalize-space(//span[contains(@class, "distfromdest_clean")])').extract_first())
                except:
                    location_from_center = "not available"
                if resultsParsed >= self.offset:
                    hotels_list[url] = location_from_center
                resultsParsed += 1
                if self.reqResults != -1 and resultsParsed >= self.reqResults + self.offset:
                    stopParse = True
                    break
            next_page_url = self.driver.find_elements_by_xpath('//a[contains(@class, "paging-next")]')
            if len(next_page_url) < 1 or stopParse:
                break
            else:
                self.driver.get(next_page_url[0].get_attribute("href"))
        
        print (hotels_list)
        print (len(hotels_list))
        hotelsParsed = 0
        for url, location_from_center in hotels_list.items():
            print("*********************Hotel " + str(hotelsParsed + 1) + " out of " + str(len(hotels_list)))
            
            #offset_list = [1, 2, 4, 5, 7, 14, 20, 25, 30, 35, 40, 45, 50, 55, 60, 70, 80, 90, 120]
            offset_list = [1, 120]
            offset_list = [1, 3, 7, 14, 21, 28, 30, 35, 42, 49, 56, 60, 63, 70, 77, 84, 90, 91, 98, 105, 112, 119, 120, 126, 133, 140, 147, 150, 154, 161, 168, 175, 180, 182, 189, 196, 203, 210, 217, 224, 231, 238, 240, 245, 252, 259, 266, 270, 273, 280, 287, 294, 300, 301, 308, 315, 322, 329, 330, 336, 343, 350, 357, 360, 364]
            start_time = time.time()
            
            for days_offset in offset_list:
                checkin_date = (datetime.datetime.today() + timedelta(days = days_offset)).strftime('%Y-%m-%d')
                checkout_date = (datetime.datetime.today() + timedelta(days = days_offset + 1)).strftime('%Y-%m-%d')
                url = self.add_params_url(url, 'checkin', checkin_date)
                url = self.add_params_url(url, 'checkout', checkout_date)

                #add 1 second delay to not get blocked by website because that would be bad lol
                time.sleep(1)
                self.driver.get(url)
                response = Selector(text=self.driver.page_source.encode('utf-8'))

                if offset_list[0] == days_offset:

                    #for first hotel iteration, do this shit
                    hotel_name = unicodedata.normalize("NFKD", response.xpath('normalize-space(//h2[@id="hp_hotel_name"]/text())').extract_first()),
                    address = unicodedata.normalize("NFKD", response.xpath('normalize-space(//span[contains(@class, "hp_address_subtitle")]/text())').extract_first()),
                    stars = str(len(response.xpath('//span[contains(@class, "hp__hotel_ratings__stars")]//circle'))),
                    rating = unicodedata.normalize("NFKD", response.xpath('normalize-space(//span[contains(@class, "review-score-widget")]/span[contains(@class, "review-score-badge")]/text())').extract_first()),

                    #check if hotel chain exists
                    is_hotel_chain = 0
                    hotel_chain_text = unicodedata.normalize("NFKD", response.xpath('normalize-space(//p[contains(@class, "hotel_meta_style")])').extract_first()).lower()
                    if 'hotel chain' in hotel_chain_text:
                        is_hotel_chain = 1

                    #check if amenities exist
                    has_parking = 0
                    has_wifi = 0
                    has_breakfast_food_drinks = 0
                    has_pool = 0
                    has_beach_front = 0
                    has_gym = 0
                    has_airport_shuttle = 0
                    summary = unicodedata.normalize("NFKD", response.xpath('normalize-space(string(//div[@id="summary"]))').extract_first()).lower()
                    facilities = unicodedata.normalize("NFKD", response.xpath('normalize-space(string(//div[contains(@class, "facilitiesChecklist")]))').extract_first()).lower()
                    if 'pool' in summary or 'pool' in facilities:
                        has_pool = 1
                    if 'gym' in summary or 'gym' in facilities or 'fitness centre' in facilities:
                        has_gym = 1
                    if 'beach front' in summary or 'beach front' in facilities:
                        has_beach_front = 1
                    if 'breakfast buffet' in summary or 'breakfast buffet' in facilities:
                        has_breakfast_food_drinks = 1
                    if 'parking' in summary or 'parking' in facilities:
                        has_parking = 1
                    if 'wifi' in facilities or 'wi-fi' in facilities:
                        has_wifi = 1
                    if 'airport shuttle' in summary or 'airport shuttle' in facilities:
                        has_airport_shuttle = 1
                    
                    #look for rooms
                rooms_list = response.xpath('//table[contains(@class, "hprt-table")]//tr')
                #for every room
                for room in rooms_list:
                    room_type =  unicodedata.normalize("NFKD", room.xpath('normalize-space(.//span[contains(@class, "hprt-roomtype-icon-link")]/text())').extract_first())
                    price =  unicodedata.normalize("NFKD", room.xpath('normalize-space(.//span[contains(@class, "hprt-price-price-standard")]/text())').extract_first())
                    if not price:
                        price =  unicodedata.normalize("NFKD", room.xpath('normalize-space(.//span[contains(@class, "hprt-price-price-actual")]/text())').extract_first())
                        if not price:
                            price =  unicodedata.normalize("NFKD", room.xpath('normalize-space(.//span[contains(@class, "bui-price__title-small")]/text())').extract_first())
                    if room_type and price:
                        capacityNum = len(room.xpath('.//div[contains(@class, "hprt-occupancy-occupancy-info")]//i'))
                        capacity = str(len(room.xpath('.//div[contains(@class, "hprt-occupancy-occupancy-info")]//i'))),
                        if (capacityNum <= 2):
                            ##yield for every room entry in available room list
                            yield {
                                'hotel_name': hotel_name,
                                'address': address,
                                'stars': stars,
                                'rating': rating,
                                'check-in-date': checkin_date,
                                'check-out-date': checkout_date,
                                'room_type': room_type,
                                'price': price,
                                'capacity': capacity,
                                'location_from_center': location_from_center,
                                'is_hotel_chain': is_hotel_chain,
                                'has_parking' : has_parking,
                                'has_wifi': has_wifi,
                                'has_breakfast_food_drinks':  has_breakfast_food_drinks,
                                'has_pool': has_pool,
                                'has_beach_front': has_beach_front,
                                'has_gym': has_gym,
                                'has_airport_shuttle': has_airport_shuttle
                            }
                            
            elapsed_time = time.time() - start_time
            time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
            print('Elapsed Time: ' + str(elapsed_time))
            hotelsParsed += 1
            
        print('Hotels Parsed: ' + str(hotelsParsed))

    def add_params_url(self, url, param, value):
        scheme, netloc, path, query_string, fragment = urlsplit(url)
        query_params = parse_qs(query_string)
        query_params[param] = [value]
        new_query_string = urlencode(query_params, doseq=True)
        return urlunsplit((scheme, netloc, path, new_query_string, fragment))

    def generate_results_url(self, url, offset):
        scheme, netloc, path, query_string, fragment = urlsplit(url)
        query_params = parse_qs(query_string)
        query_params['rows'] = ['15']
        query_params['offset'] = [offset]
        new_query_string = urlencode(query_params, doseq=True)
        return urlunsplit((scheme, netloc, path, new_query_string, fragment))
        

    def spider_closed(self, spider):
        if self.driver:
            self.driver.quit()
