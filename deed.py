import datetime
import re
import scrapy

class TauntonSpider(scrapy.Spider):
    name = 'taunton'

    def start_requests(self):
        urls = ['http://www.tauntondeeds.com/Searches/ImageSearch.aspx']
        for url in urls:
            yield scrapy.Request(url, callback=self.parse)
            
    def parse(self, response):
        for i in range(datetime.datetime.now().month):
            yield scrapy.FormRequest.from_response(
                response,
                formdata={
                    'ctl00$cphMainContent$txtLCSTartDate$dateInput': '2020-0'+str(i+1)+'-02-00-00-00',
                    'ctl00$cphMainContent$txtLCEndDate$dateInput': '2020-0'+str(i+2)+'-01-00-00-00',
                    'ctl00$cphMainContent$ddlLCDocumentType$vddlDropDown': '101627',
                    'ctl00$cphMainContent$btnSearchLC': 'Search+Land+Court'},
                callback=self.parse_table)
# переход по страницам организовать не удалось, по этому запрос идет по месяцам
# с августа перестанет работать. пропускает сделки за первое января

    def parse_table(self, response):
        i = -1
        for grid in response.xpath('//tr[@class="gridRow" or @class="gridAltRow"]'):
            i += 1
            yield {
                'date': grid.xpath('//tr[@class="gridRow" or @class="gridAltRow"]/td[2]/text()')[i].get(),
                'type': grid.xpath('//tr[@class="gridRow" or @class="gridAltRow"]/td[3]/text()')[i].get(),
                'book': None,
                'page_num': None,
                'doc_num': grid.xpath('//tr[@class="gridRow" or @class="gridAltRow"]/td[6]/text()')[i].get(), 
                'city': grid.xpath('//tr[@class="gridRow" or @class="gridAltRow"]/td[7]/text()')[i].get(), 
                'description': grid.xpath('//tr[@class="gridRow" or @class="gridAltRow"]/td[8]/span/text()')[i].get(),
                'cost': self.parse_reg_cost(grid.xpath('//tr[@class="gridRow" or @class="gridAltRow"]/td[8]/span/text()')[i].get()),
                'street_address': self.parse_reg_str_ad(grid.xpath('//tr[@class="gridRow" or @class="gridAltRow"]/td[8]/span/text()')[i].get()),
                'zip': None,
                'state': None}
# i нужно потомучто в каждый grid почемуто попадают все селекторы страница,
# хотя по идее должны быть только селекторы строки
# date в формате str т.к. datetime упоминаемый в задании не является встроенным типом данных
# book, page_num, zip, state всегда отсутствуют
# 'page_num': grid.xpath('//tr[@class="gridRow" or @class="gridAltRow"]/td[5]/text()')[i].get(), 
# 'book': grid.xpath('//tr[@class="gridRow" or @class="gridAltRow"]/td[4]/text()')[i].get(),

    def parse_reg_cost(self, text): # парсит сумму, если указана
        if re.search(r"(\d+\.\d\d)", text) is not None:
            return float(re.findall(r"(\d+\.\d\d)", text)[0])
        else:
            return None

    def parse_reg_str_ad(self, text): # парсит несколько вариантов адреса
        if re.search(r"(\d+\s\D+\s(RD|DR|ST|AVE|WAY|LANE))\s,\s\$", text) is not None:
            return str(re.findall(r"(\d+\s\D+\s(RD|DR|ST|AVE|WAY|LANE))\s,\s\$", text)[0][0])
        elif re.search(r"(\s\D+\s(RD|DR|ST|AVE|WAY|LANE))\s,\s\$", text) is not None:
            return str(re.findall(r"(\s\D+\s(RD|DR|ST|AVE|WAY|LANE))\s,\s\$", text)[0][0])
        elif re.search(r"(\d+\s\D+\s(RD|DR|ST|AVE|WAY|LANE))\s", text) is not None:
            return str(re.findall(r"(\d+\s\D+\s(RD|DR|ST|AVE|WAY|LANE))\s", text)[0][0])
        else:
            return None
