# -*- coding: utf-8 -*-

# import numpy as np
# import pandas as pd
# from scrapy.selector import Selector
# import requests
# from datetime import datetime
# from sqlalchemy import create_engine
# engine = create_engine('mysql://root:@localhost/fund')

# code = '003325'
# start_date = '2017-01-01'
# end_date = datetime.today().strftime('%Y-%m-%d')
# per = 10
# url = 'http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&code={code}&page=1&per={per}&sdate={sdate}&edate={edate}'\
#     .format(code=code, per=per, sdate=start_date, edate=end_date)
# response = requests.request('GET', url).content
#
# date_list = Selector(text=response).xpath('//tr//td[1]/text()').extract()
# price_list = Selector(text=response).xpath('//tr//td[2]/text()').extract()
#
# print date_list
# print price_list
#
# price_df = pd.DataFrame()
# price_df['data_date'] = date_list
# price_df['price'] = pd.Series(price_list)
# price_df['code'] = code
#
# print price_df

# price_df['code'] = code
# price_df.drop(['bstatus', 'sstatus'], axis=1, inplace=True)
# price_df['growth_rate'] = price_df['growth_rate'].map(lambda x: x.rstrip('%'))
# print price_df


