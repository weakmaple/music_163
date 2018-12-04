from scrapy import cmdline

gedan_url = input("请输入歌单链接：").strip()
cmdline.execute(str("scrapy crawl music_spider -a gedan_url=%s"%(gedan_url,)).split())
# cmdline.execute('scrapy crawl music_spider'.split())