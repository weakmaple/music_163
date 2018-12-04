# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import requests, click, base64, binascii, json, os
from Crypto.Cipher import AES
from http import cookiejar
from music163.settings import DEFAULT_REQUEST_HEADERS

class Music163Pipeline(object):

    def process_item(self, item, spider):
        #下载路径
        path = './'
        gedang_name = os.path.join(path, item['big_title'])
        if not os.path.exists(gedang_name):
            os.mkdir(gedang_name)

        song_id = item['song_ids']
        song_title = item['song_title']

        #将每一首歌的id进行解码，获得下载的url链接
        csrf = ''
        bit_rate = 320000
        url = 'http://music.163.com/weapi/song/enhance/player/url?csrf_token='
        params = {'ids': [song_id], 'br': bit_rate, 'csrf_token': csrf}
        crawl = Crawler()
        result = crawl.post_request(url, params)
        result_url = result['data'][0]['url']

        #获得下载的url之后，便可以开始真正下载了
        response = requests.session()
        resp = response.get(result_url,stream=True)
        with open(gedang_name+r'\\'+song_title+'.mp3','wb') as fp:
            for chunk in resp.iter_content(chunk_size=1024):
                if chunk:
                    fp.write(chunk)
        return item

#下面这一部分是github上的大佬写的，用于破解网易云音乐链接的命名方式，看起来应该是涉及到AES了
#这部分没有专业知识应该是看不懂的，有兴趣的朋友可以研究一下
#github大佬的网址是：https://github.com/Jack-Cherish/python-spider/tree/master/Netease
#顺便一提 这位大佬有很多爬虫的项目 可以学习一下
class Encrypyed():
    #解密算法
    def __init__(self):
        self.modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
        self.nonce = '0CoJUm6Qyw8W8jud'
        self.pub_key = '010001'
    # 登录加密算法, 基于https://github.com/stkevintan/nw_musicbox脚本实现
    def encrypted_request(self, text):
        text = json.dumps(text)
        sec_key = self.create_secret_key(16)
        enc_text = self.aes_encrypt(self.aes_encrypt(text, self.nonce), sec_key.decode('utf-8'))
        enc_sec_key = self.rsa_encrpt(sec_key, self.pub_key, self.modulus)
        data = {'params': enc_text, 'encSecKey': enc_sec_key}
        return data

    def aes_encrypt(self, text, secKey):
        pad = 16 - len(text) % 16
        text = text + chr(pad) * pad
        encryptor = AES.new(secKey.encode('utf-8'), AES.MODE_CBC, b'0102030405060708')
        ciphertext = encryptor.encrypt(text.encode('utf-8'))
        ciphertext = base64.b64encode(ciphertext).decode('utf-8')
        return ciphertext

    def rsa_encrpt(self, text, pubKey, modulus):
        text = text[::-1]
        rs = pow(int(binascii.hexlify(text), 16), int(pubKey, 16), int(modulus, 16))
        return format(rs, 'x').zfill(256)

    def create_secret_key(self, size):
        return binascii.hexlify(os.urandom(size))[:16]

class Crawler():
    def __init__(self, timeout=60, cookie_path='.'):
        self.session = requests.Session()
        self.session.headers.update(DEFAULT_REQUEST_HEADERS)
        self.session.cookies = cookiejar.LWPCookieJar(cookie_path)
        self.download_session = requests.Session()
        self.timeout = timeout
        self.ep = Encrypyed()

    def post_request(self, url, params):
        data = self.ep.encrypted_request(params)
        resp = self.session.post(url, data=data, timeout=self.timeout)
        result = resp.json()
        # print(resp.url)
        if result['code'] != 200:
            click.echo('post_request error')
        else:
            return result
