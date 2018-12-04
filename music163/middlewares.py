# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import scrapy
class Music163DownloaderMiddleware(object):
    #rrequest的请求被传到这里，接下来使用webdriver进行解析，然后再把响应返回给parse_catalog
    def process_request(self, request, spider):
        ids = request.url.split('=')[-1]
        url = 'https://music.163.com/#/playlist?id=%s' % ids
        spider.driver.get(url)
        #注意：下面这一条代码很重要，因为webdriver无法显示出iframe中的东西
        #所以需要使用switch_to.frame('g_iframe')来将隐藏的内容找出来
        spider.driver.switch_to.frame('g_iframe')
        source = spider.driver.page_source
        return scrapy.http.HtmlResponse(url=url,body=source,encoding="utf-8",request=request)


