# -*- coding: UTF-8 -*-
"""
Created on 2017年11月10日
@author: Leo
"""

# 系统库
import datetime
import json
import time
import urllib.parse as up

# 第三方库
import scrapy
from scrapy.conf import settings


# 商事主体公司年报基本信息 ID=52776 Total=1870025
class BusinessYearReport(scrapy.Spider):
    name = "business_information_year"

    def __init__(self, **kwargs):
        # 起始地址
        self.start_urls = ['http://datagz.gov.cn/data/catalog/detail.do?method=QueryDataItem&']

        # 请求页面拼接的数据
        self.post_data = {
            "cata_id": str(settings['YEAR_INFO_ID']),  # 目录号
            "rows": str(settings['MAX_ROWS_PER_PAGE']),  # 每页的数据量
            "page": settings['DEFAULT_BEGIN_PAGE_NUM'],  # 页码
        }

        # super方法
        super().__init__(**kwargs)

    def start_requests(self):
        # 请求链接
        post_url = self.start_urls[0] + up.urlencode(self.post_data)
        yield scrapy.Request(url=post_url, method="POST", callback=self.parse)

    def parse(self, response):
        # 获取数据
        businesses_year_report = json.loads(bytes.decode(response.body))

        # 判断是否数据为空
        if len(businesses_year_report['rows']) == 0:
            scrapy.Spider.close(BusinessYearReport, reason="All data has been collected.")

        # 解析数据
        for year_report in businesses_year_report['rows']:
            # 添加数据年份和最近更新的时间戳
            year_report.update(dict(statistics_year=datetime.datetime.now().year))
            year_report.update(dict(last_update_time=int(time.mktime(datetime.datetime.now().timetuple())) * 1000))
            data_item = year_report
            yield data_item

        # 最大上限页数
        max_page = businesses_year_report['total']
        if self.post_data['page'] + 1 <= max_page:
            self.post_data['page'] += 1
            post_url = self.start_urls[0] + up.urlencode(self.post_data)
            yield scrapy.Request(url=post_url, method="POST", callback=self.parse)
        else:
            scrapy.Spider.close(BusinessYearReport, reason="All data has been collected.")

