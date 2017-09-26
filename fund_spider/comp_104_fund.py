# -*- coding: utf-8 -*-

from fund_spider.spiders.fund_spider import FundSpider


class CompSpider(FundSpider):
    con_log = ''

    def closed(self, reason):
        pass

f = open('connection_104_log.txt', 'r')
code_list = f.read().splitlines()
print code_list

f2 = open('fix_connection_104_error_log.txt', 'w')
spider = CompSpider()
while code_list != []:
    code = code_list[0]
    status = spider.to_price_list(code)
    if status != 'ConnectionError 104':
        code_list.remove(code)
        f2.write(code + '\t' + status + '\n')

f.close()
f2.close()
