#coding=utf-8
import re
import json
import scrapy
import urllib
from scrapy.selector import Selector
try:
    from scrapy.spider import Spider
except:
    from scrapy.spider import BaseSpider as Spider
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor as sle
from cnblogs.items import *


class CnblogsSpider(CrawlSpider):
    #定义爬虫的名称
    name = "CnblogsSpider"
    #定义允许抓取的域名,如果不是在此列表的域名则放弃抓取
    allowed_domains = ["cnblogs.com"]
    #定义抓取的入口url
    start_urls = [
       "http://www.cnblogs.com/rwxwsblog/default.html?page=1"
    ]
    # 定义爬取URL的规则，并指定回调函数为parse_item
    rules = [
        Rule(sle(allow=("/rwxwsblog/default.html\?page=2")), #\d{1,}此处要注意?号的转换，复制过来需要对?号进行转换。
          follow=True,
          callback='parse_item')
    ]
    print "**********CnblogsSpider**********"
    #定义回调函数
    #提取数据到Items里面，主要用到XPath和CSS选择器提取网页数据
    def parse_item(self, response):
        #print "-----------------"

        sel = Selector(response)
        base_url = get_base_url(response)
        postTitle = sel.css('div.day div.postTitle')
        #print "=============length======="
        postCon = sel.css('div.postCon div.c_b_p_desc')
       #标题、url和描述的结构是一个松散的结构，后期可以改进
        for index in range(len(postTitle)):
            item = CnblogsItem()
            item['title'] = postTitle[index].css("a").xpath('text()').extract()[0]
            #print item['title'] + "***************\r\n"
            item['link'] = postTitle[index].css('a').xpath('@href').extract()[0]
            item['listUrl'] = base_url
            item['desc'] = postCon[index].xpath('text()').extract()[0]
            #print base_url + "********\n"

            #print repr(item).decode("unicode-escape") + '\n'

            yield scrapy.Request(item['link'] , self.parse_details , meta={'item': item})

            # print repr(item).decode("unicode-escape") + '\n'


    def parse_details(self , response):
        items = []
        content1 = []
        item = response.meta['item']

        sel = Selector(response)
        #html =repr(sel.xpath('//html').extract()[0]).decode("unicode-escape")
        #html = repr(sel.xpath('//html').extract()[0]).decode("unicode_escape")
        #html =response.xpath('//div[@id="cnblogs_post_body"]/*').extract()
        #html =response.xpath('//div[@id="cnblogs_post_body"]//node()').extract()

        html="".join(response.xpath('//html').extract())

       # content = sel.xpath('//div[@class="post"]//text()').extract()[0].encode('utf-8')
        #content = repr(sel.xpath('//div[@class="post"]//text()')j.extract()).decode("unicode-escape").encode('utf-8')
       # content = repr(sel.xpath('//div[@class="post"]//text()').extract()).decode("unicode-escape")

        #content = "".join(response.xpath('//div[@class="post"]//text()').extract())

        content = "".join(response.xpath('//div[@id="cnblogs_post_body"]//text()').extract())


        #print 'html:'+html.decode("unicode-escape")
        #print 'html:' + html.encode('utf-8')
        #print 'content:' + content

       # print urllib.unquote(str(html))
        #print 'content:' + content.encode('raw_unicode_escape')

        #content = repr(sel.xpath('//div[@class="post"]//text()').extract())
        #
        #
        #
        # for t in content:
        #     #content1.append(t.encode("utf-8"))
        #     print(t.encode("utf-8"))
        #content = repr(sel.xpath('//div[@class="post"]//text()').extract())
       # content =repr(sel.xpath('//div[@class="post"]//text()').extract().encode('utf-8'))

        #content = repr(sel.css('div.post').xpath('text()').extract()).decode("unicode-escape")
        #content = unicode.encode( content , 'utf-8')

        #content='content'#repr(content).decode("unicode-escape")
        item['html'] =html
        item['content'] = content

        print 'link::'+item['link']
        print 'desc::'+item['desc']

        #str = json.dumps(html, ensure_ascii=False) + "\n";
        #str = unicode.decode(str, 'utf-8').encode('gb2312');

        #s=html#item['content']
        #print 'html:' + html

        #
        # if isinstance(s, unicode):
        #     # s=u"中文"
        #     print s.encode('utf-8')
        # else:
        #     # s="中文"
        #     print s.decode('utf-8').encode('gb2312')


        #print 'content:' + item['content']
        # populate more `item` fields
        items.append(item)

        return items