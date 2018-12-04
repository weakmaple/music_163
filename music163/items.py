# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class Music163Item(scrapy.Item):
    # define the fields for your item here like:
    #song_ids是歌曲的id
    #song_title是歌曲的名字
    #big_title是歌单的名字
    song_ids = scrapy.Field()
    song_title = scrapy.Field()
    big_title = scrapy.Field()
