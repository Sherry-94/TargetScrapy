from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from scrapy.http import FormRequest, Request
import re
import math
import sys
import base64
import time
import json
reload(sys)
sys.setdefaultencoding("utf_8")
sys.getdefaultencoding()

from TargetScraper.items import TargetmergedItem

class mySpider(BaseSpider):
    name = 'spidey'

    allowed_domains = ["target.com"]

    start_urls = ['http://www.target.com/']
    #start_urls = ['http://www.target.com/np/more/-/N-5xsxf#?lnk=ct_menu_13_20&intc=1865103|null']

    def SearchResult(self,response):

        fixedUrl='http://tws.target.com/searchservice/item/search_results/v2/by_keyword?callback=getPlpResponse&sort_by=Featured&zone=PLP&facets=&category='
        pageCount=0
        #offset=0
        categoryPath = '//link[@rel="canonical"]/@href'
        category = response.selector.xpath(categoryPath).extract()
        print category
        category = str(category)
        category = category.split('/N-', 1)[-1]
        category = category.replace("'", "").replace("[u","").replace("]","").replace("[","")

        isLeafPath = '//input[@id="isLeaf"]/@value'
        isLeaf = response.selector.xpath(isLeafPath).extract()
        print isLeaf
        isLeaf = str(isLeaf)
        isLeaf = isLeaf.replace("'", "").replace("[u", "").replace("]", "").replace("[", "")
        print isLeaf


        fullRequest = fixedUrl+ str(category) + '&page=' + str(int(pageCount)+1) + '&response_group=Items%2CVariationSummary&isLeaf=' + str(isLeaf)
        myRequest = Request(fullRequest, callback=self.Pagination, meta={'Category': category})
        yield myRequest


    def Pagination(self, response):

        category = response.meta['Category']
        fixedUrl='http://tws.target.com/searchservice/item/search_results/v2/by_keyword?callback=getPlpResponse&sort_by=Featured&zone=PLP&facets=&category='
        completePage = response.xpath("//*").extract()
        completePage = str(completePage.pop(0))
        NoOfPagesIndex = completePage.rfind('totalPages')
        newPage =  completePage[NoOfPagesIndex+len("totalPages"):]
        Index = newPage.index(':')
        newPage = newPage[Index:]
        Index = newPage.index('"')
        newPage = newPage[Index+1:]
        Index = newPage.index('"')
        NoOfPages = newPage[:Index]
        print NoOfPages
        NoOfHits = int(NoOfPages)-1



        itemNumbers = []

        while "tcin" in completePage:
            item = TargetmergedItem()
            index = completePage.index("tcin")
            completePage = completePage[index + len("tcin"): ]
            index = completePage.index(':')
            completePage = completePage[index:]
            index = completePage.index('"')
            completePage = completePage[index+1:]
            index = completePage.index('"')
            a = completePage[:index]
            #print a
            item['ItemNumbers'] = a
            itemNumbers.append(item)

        pageCount=1


        if NoOfHits ==0:
            fullRequest=fixedUrl+ str(category) + '&page=' + str(pageCount) + '&response_group=Items%2CVariationSummary&isLeaf=false'
            myRequest = Request(fullRequest, callback=self.SinglePage,meta={'list':itemNumbers})
            yield myRequest


        else:
             for i in range(NoOfHits):
                if i==0:
                    fullRequest=fixedUrl+ str(category) + '&page=' + str(int(pageCount)+(i+1)) + '&response_group=Items%2CVariationSummary&isLeaf=false'
                    myRequest = Request(fullRequest, callback=self.ItemNumbers,meta={'list':itemNumbers})
                    yield myRequest

                else:

                    #print {"page is",i}
                    fullRequest=fixedUrl+ str(category) + '&page=' + str(int(pageCount)+(i+1)) + '&response_group=Items%2CVariationSummary&isLeaf=false'
                    myRequest = Request(fullRequest, callback=self.ItemNumbersNext)
                    yield myRequest




    def SinglePage(self,response):

        items = response.meta['list']
        return items


    def ItemNumbers(self,response):
        items = response.meta['list']


        completePage = response.xpath("//*").extract()
        completePage = str(completePage.pop(0))


        Index = 0
        #itemNumbers = []

        while "tcin" in completePage:
            item = TargetmergedItem()
            index = completePage.index("tcin")
            completePage = completePage[index + len("tcin"): ]
            index = completePage.index(':')
            completePage = completePage[index:]
            index = completePage.index('"')
            completePage = completePage[index+1:]
            index = completePage.index('"')
            a = completePage[:index]
            item['ItemNumbers'] = a
            #print a
            items.append(item)

        return items



    def ItemNumbersNext(self,response):



        completePage = response.xpath("//*").extract()
        completePage = str(completePage.pop(0))


        Index = 0
        itemNumbers = []

        while "tcin" in completePage:
            item = TargetmergedItem()
            index = completePage.index("tcin")
            completePage = completePage[index + len("tcin"): ]
            index = completePage.index(':')
            completePage = completePage[index:]
            index = completePage.index('"')
            completePage = completePage[index+1:]
            index = completePage.index('"')
            a = completePage[:index]
            item['ItemNumbers'] = a
            #print a
            itemNumbers.append(item)

        return itemNumbers


#################################################################################################################################################################################

    def parse(self, response):

        file = open('urls.txt','r')
        urls = file.readlines()
        #itemNumbers = itemNumbers.strip()
        for url in urls:
            fixedRequest = url.strip()
            myRequest = Request(fixedRequest, callback=self.SearchResult)
            yield myRequest
























        #
        # urlPaths = "//ul[@class='first']/li/ul/li/a/@href"
        # urls = response.selector.xpath(urlPaths).extract()
        # #
        # # for url in urls:
        # #     if "np/more" in str(url):
        # #         print "shit"
        # #
        # #     else:
        # #
        # #         url = url.replace("%7C","|").replace("%20"," ")
        # #         print url
        #
        #
        # for url in urls:
        #
        #     url = url.replace("%7C","|").replace("%20"," ")
        #     if "np/more" in str(url):
        #         print "shit"
        #     elif "toys" in str(url):
        #         print 'ignore'
        #     else:
        #         if "target" not in url:
        #             myRequest = Request("http://www.target.com"+url, callback=self.treversal)
        #         else:
        #             myRequest = Request(url, callback=self.treversal)
        #         yield myRequest


         # urlPaths = "//div[@class='ul-wrapper']/ul/li/a/@href"
        # urls = response.selector.xpath(urlPaths).extract()
        #
        # # for url in urls:
        # #     url = url.replace("%7C","|")
        # #     print url
        #
        #
        # for url in urls:
        #     url = url.replace("%7C","|").replace("%20"," ")
        #     if "target" not in url:
        #         myRequest = Request("http://www.target.com"+url, callback=self.treversal)
        #     else:
        #         myRequest = Request(url, callback=self.treversal)
        #     return myRequest

        #urlPaths = "//div[@class='ul-wrapper']/ul/li/a/@href"















































