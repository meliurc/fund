# -*- coding: utf-8 -*-

from datetime import date, timedelta
import requests
from requests.adapters import ConnectionError
import pandas as pd
import scrapy
from scrapy.spider import Spider
from scrapy.selector import Selector
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

mysql_engine = create_engine('mysql://root:@localhost/fund')


class FundSpider(Spider):
    name = 'price_d'
    start_urls = ['http://fund.eastmoney.com/company/default.html']

    cookies = {'st_pvi': ''}
    con_log = open('connection_104_log.txt', 'w')

    def __init__(self, sdate, edate, table):
        super(FundSpider, self).__init__()
        """
        :param sdate: string, YYYY-mm-dd
        :param edate: string, YYYY-mm-dd
        """
        self.sdate=sdate
        self.edate=edate
        self.table=table

    def parse(self, response):
        href_list = response.xpath('//td[@class="td-align-left"]/a/@href').extract()
        for href in href_list:
            url = response.urljoin(href)
            request = scrapy.Request(url, self.parse_company_page, dont_filter=True, cookies=self.cookies)
            yield request

    def parse_company_page(self, response):
        name_list = response.xpath('//td[@class="fund-name-code"]/a[1]/text()').extract()
        code_list = response.xpath('//td[@class="fund-name-code"]/a[2]/text()').extract()
        href_list = response.xpath('//td[@class="fund-name-code"]/a[2]/@href').extract()
        for code in code_list:
            yield self.to_price_list(code)

    def to_price_list(self, code):
        start_date = self.sdate
        end_date = self.edate
        per = 366
        url = 'http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&code={code}&page=1&per={per}&sdate={sdate}&edate={edate}'\
            .format(code=code, per=per, sdate=start_date, edate=end_date)

        try:
            price_js = requests.request('GET', url).content
        except ConnectionError:
            self.con_log.write(code + '\n')
            return 'ConnectionError 104'

        date_list = Selector(text=price_js).xpath('//tr//td[1]/text()').extract()
        price_list = Selector(text=price_js).xpath('//tr//td[2]/text()').extract()
        if len(date_list) == 0 or len(price_list) == 0:
            return 'NoDataWarning'

        return self.to_price_df(code, date_list, price_list)

    def to_price_df(self, code, date_list, price_list):
        price_df = pd.DataFrame()
        price_df['data_date'] = pd.Series(date_list)
        price_df['price'] = pd.Series(price_list)
        price_df['code'] = code

        return self.to_mysql(price_df)

    def to_mysql(self, price_df):
        try:
            price_df.to_sql(self.table, mysql_engine, if_exists='append', index=False)
            return 0
        except UnicodeEncodeError:
            price_df.to_csv('./unicode_error/unicode_error_{}.txt'.format(str(price_df['code'][0])))
            return 'UnicodeEncodeError'
        except OperationalError:
            return 'Database OperationalError'

        # price_df.to_csv('output.txt', sep='\t', header=False, index=False, mode='a')

    def closed(self, reason):
        self.con_log.close()













