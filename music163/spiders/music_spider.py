# -*- coding: utf-8 -*-
import re
import scrapy
from selenium import webdriver
from music163.items import Music163Item

class MusicSpiderSpider(scrapy.Spider):
    name = 'music_spider'
    allowed_domains = ['music.163.com']
    start_urls = ['http://music.163.com/']
    # first_url = 'https://music.163.com/#/playlist?id=107391599'
    driver = webdriver.Chrome()
    driver.set_page_load_timeout(30)

    def __init__(self,gedan_url=None, *args, **kwargs):
        self.first_url = gedan_url

    #获得歌单链接之后，交给parse_catalog解析，但这里有开启中间件（middlewares.py）
    #所以请求会先被传去middlewares.py
    def start_requests(self):
        yield scrapy.http.Request(url=self.first_url,callback=self.parse_catalog)

    def closed(self, spider):
        self.driver.close()

    #这里将歌单中每一首个的id和名字传到piplines.py进行处理
    def parse_catalog(self, response):
        # print(response.text)
        songs_list = response.xpath('//table[@class="m-table "]/tbody/tr')
        big_title = response.xpath('//h2[@class="f-ff2 f-brk"]/text()').get()
        big_title = re.sub(r'[<>:"/\\|?*]', '', big_title)
        for song in songs_list:
            song_href = 'https://music.163.com/#'+song.xpath('.//a/@href').get()
            song_title = song.xpath('.//b/@title').get()
            song_ids = re.split('=',song_href)[-1]
            song_title = re.sub(r'[<>:"/\\|?*]', '', song_title)
            item = Music163Item(song_ids = song_ids,song_title = song_title,big_title=big_title)
            yield item

