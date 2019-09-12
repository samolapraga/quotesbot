import scrapy
import logging
import re
from google.cloud import translate 
from scrapy.selector import Selector
from scrapy.item import Item
from scrapy.http import FormRequest
from quotesbot.items import Product

class Bikeoutlet(scrapy.Spider):
	name = "bikeoutlet"
#	allowed_domains = ["bikeoutlet.cz"]
	start_url = "https://www.bikeoutlet.cz/bikeoutlet.php?disp=akce"
	login_url = "https://www.bikeoutlet.cz/prihlaseni.php"
	generic_url = "https://www.bikeoutlet.cz/index.php"
	wks = ""
	
	def start_requests(self):
		self.logger.info("This is before ZZZZZZZ")
		# scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
		# credentials = ServiceAccountCredentials.from_json_keyfile_name('ScrapBikeOutlet.json', scope)
		# gc = gspread.authorize(credentials)
		# self.wks = gc.open("BOScrap").sheet1
		yield scrapy.FormRequest(url=self.generic_url, callback=self.parse)
		
	def parse(self, response):
		self.logger.info("This is before XXXXXXXXXX %s", response.url)
		return scrapy.FormRequest(url=self.login_url, method="POST", formdata={"data[ico]": "RO33651056", "data[heslo]": "k!cka555"},callback=self.after_login)
		
	def after_login(self, response):
		self.logger.info("Got after_login %s", response.url)
		return scrapy.FormRequest(url=self.start_url, cookies={'userico' : 'RO33651056'}, callback=self.parse_pages)
		
	def parse_pages(self, response):
		pages = []
		pages = response.css('div[style="clear: both;"] + p > a::attr(href)').getall()
		#pages.add(self.start_url)
		pages.insert(0,self.start_url)
		for page in pages:
			yield scrapy.FormRequest(url=page, cookies={'userico' : 'RO33651056'}, callback=self.parse_page)
			
	def parse_page(self, response):
		hxs = Selector(response)
		listitem = response.css('div.item_list.item_list_akce')
		products = []
		for item in listitem:
			prod = Product()
			prod['id'] = item.css('div.ceny::text').get()
			prod['id'] = re.sub('[^0-9]','', prod['id'])
			prod['desc'] = item.css('div.item_list_desc1::text').get()
			prod['desc'] = prod['desc'].replace('\n','')
			prod['desc'] = prod['desc'].replace('\t','')
			#prod['longdesc'] = ""
			descr = item.css('div.item_list_desc2 *::text').getall()
			prod['longdesc'] = '\n'.join(descr)
				# prod['longdesc'] = prod['longdesc'].join(descr)
			prod['regprice'] = item.css('span.item_type_cena_bezna > span::text').get()
			#prod['regprice'] = item.xpath('//span[.="price exclusive of VAT"]::text()')
			prod['price'] = item.css('span::text').get()
			if 'cena' in prod['price']:
				prod['price'] = item.css('span[style*="background-color: rgb(204,0,0);"]::text').get()
				if prod['price'] is None:
					prod['price'] = item.css('span.nase_cena::text').get()
			prod['stock'] = item.css('img[src*="skladem_cz_yes.png"]').get()
			if prod['stock'] is not None:
				prod['stock'] = True
			prod['img'] = item.css('img[class="item_list_icon"]::attr(src)').get()
			products.append(prod)
		return products
	