# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import gspread
import time
from oauth2client.service_account import ServiceAccountCredentials

class QuotesbotPipeline(object):
	wks = ""
	
	def next_available_row(worksheet):
		str_list = filter(None, worksheet.col_values(1))
		return str(len(str_list)+1)


	def open_spider(self, spider):
		#self.logger.info("Initialize Gsheet access at open_spider")
		scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
		credentials = ServiceAccountCredentials.from_json_keyfile_name('ScrapBikeOutlet.json', scope)
		gc = gspread.authorize(credentials)
		self.wks = gc.open("BOScrap").sheet1
	
	def process_item(self, item, spider):
		
		ids = self.wks.row_values(1)
		try:
			cell = self.wks.find(item['id'])
		except gspread.exceptions.CellNotFound:
			#next_row = self.next_available_row(self.wks)
			str_list = list(filter(None, self.wks.col_values(1)))
			next_row = str(len(str_list)+1)
			self.wks.update_cell(next_row, 1, item['id'])
			self.wks.update_cell(next_row, 3, item['longdesc'])
			self.wks.update_cell(next_row, 2, item['desc'])	
			self.wks.update_cell(next_row, 4, item['price'])
			self.wks.update_cell(next_row, 5, item['regprice'])
			self.wks.update_cell(next_row, 6, item['stock'])
			self.wks.update_cell(next_row, 7, item['img'])
		
		#if cell.row is not None:
		else:
			#self.wks.update_cell(cell.row, 2, item['desc'])
			#self.wks.update_cell(cell.row, 3, item['longdesc'])
			self.wks.update_cell(cell.row, 4, item['price'])
			self.wks.update_cell(cell.row, 5, item['regprice'])
			self.wks.update_cell(cell.row, 6, item['stock'])
		
		time.sleep(9)		
		return item
