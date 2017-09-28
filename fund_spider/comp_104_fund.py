# -*- coding: utf-8 -*-

import argparse
from datetime import date, timedelta
from fund_spider.spiders.fund_spider import FundSpider

parser = argparse.ArgumentParser(description='get date.')
parser.add_argument('today')
args = parser.parse_args()
today = args.today


class CompSpider(FundSpider):
    pass

f = open('connection_104_log_bak.txt', 'r')
code_list = f.read().splitlines()
print code_list

f2 = open('fix_connection_104_error_log.txt', 'w')

# today = (date.today() - timedelta(1)).strftime('%Y-%m-%d')
spider = CompSpider(sdate=today, edate=today, table='price_today')
while code_list != []:
    code = code_list[0]
    status = spider.to_price_list(code)
    if status != 'ConnectionError 104':
        code_list.remove(code)
        f2.write(str(code) + '\t' + str(status) + '\n')

f.close()
f2.close()
