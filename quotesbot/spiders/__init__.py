# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import scrapy

class bikeoutlet(scrapy.Spider):
    name = 'bikeoutlet'

    def start_requests(self):
        yield scrapy.Request('https://www.bikeoutlet.cz/bikeoutlet.php?disp=akce') 
#		% self.category)
