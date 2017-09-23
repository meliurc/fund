# -*- coding: utf-8 -*-

from fund_spider.spiders.fund_spider import FundSpider


class CompSpider(FundSpider):
    pass

f = open('scrapy.cfg', 'r')
code_list = f.read().splitlines()

spider = CompSpider()
while code_list != []:
    code = code_list[0]
    status = spider.to_price_list(code)
    print status
    if status != 'ConnectionError 104':
        code_list.remove(code)
