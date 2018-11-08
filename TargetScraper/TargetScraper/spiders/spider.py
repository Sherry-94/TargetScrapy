from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from scrapy.http import FormRequest, Request
import re
import math
import sys
import base64
import time
#import json
reload(sys)
sys.setdefaultencoding("utf_8")
sys.getdefaultencoding()


from TargetScraper.items import TargetscraperItem



class mySpider(BaseSpider):
    name = 'zeus'

    allowed_domains = ["target.com"]


    start_urls = ['http://www.target.com/']


    def parse(self, response):
        file = open('itemNumbers.txt','r')
        itemNumbers = file.readlines()
        #itemNumbers = itemNumbers.strip()


        for item in itemNumbers:
            fixedRequest = "http://www.target.com/s?searchTerm=" + item.strip() + "&category=0%7CAll%7Cmatchallpartial%7Call+categories&lnk=snav_sbox_" + item.strip()
            myRequest = Request(fixedRequest.strip() , callback=self.SearchResult)
            yield myRequest


    def SearchResult(self, response):
        itemPageUrl = response.selector.xpath('//a[@class="productClick productTitle"]/@href').extract()
        itemPageUrl = itemPageUrl.pop(0)


        if "target" not in itemPageUrl:
            myRequest = Request("http://www.target.com"+itemPageUrl, callback=self.itemPage)
        else:
            myRequest = Request(itemPageUrl, callback=self.itemPage)
        return myRequest

    def itemPage(self, response):
        item = TargetscraperItem()

        Price = response.selector.xpath("//span[@class='offerPrice']/text()").extract()
        if Price != []:
            Price = Price.pop(0)
            item['Price'] = Price
        #print Price

        Title = response.selector.xpath("//span[@class='fn']/text()").extract()
        if Title != []:
            Title = Title.pop(0)
            Title = Title.replace("\\t","").replace("[","").replace("u'","").replace("]","").replace("\\n","").decode("utf_8")
            item['Title'] = Title
        #print Title.replace("\\t","")

        Breadcrums = response.selector.xpath("//div[@id='breadcrumbs']/span/a/text()").extract()
        Breadcrums = str(Breadcrums)
        Breadcrums = Breadcrums.replace("  ","").replace("\\t","").replace("[","").replace("u'","").replace("]","").replace('u"','').replace("\\n","").replace('"','').replace("'","").decode("utf_8")
        item['Breadcrums'] = Breadcrums

        #for Breadcrum in Breadcrums:
            #print " > " + Breadcrum.replace(" ","")

        descriptionParagraph = response.selector.xpath("//div[@class='details-copy']/p/span/text()").extract()
        if descriptionParagraph != []:
            descriptionParagraph = descriptionParagraph.pop(0)
            descriptionParagraph = str(descriptionParagraph)
            descriptionParagraph = descriptionParagraph.replace("\\t","").replace("[","").replace("u'","").replace("]","")
            #print descriptionParagraph.replace("[","").replace("u'","").replace("]","")
        else:
            descriptionParagraph = str(descriptionParagraph)
            descriptionParagraph = descriptionParagraph.replace("\\t","").replace("[","").replace("u'","").replace("]","")

        descriptionListing = response.selector.xpath("//ul[@class='normal-list']/li/p").extract()
        descriptionListing = str(descriptionListing)
        descriptionListing = descriptionListing.replace("<b>","").replace("</b>","").replace("<p>","").replace("</p>","").replace("\\t","").replace("[","").replace("u'","").replace("]","").replace("'","")
        #for li in descriptionListing:
            #print str(li.replace("<b>","").replace("</b>","").replace("<p>","").replace("</p>",""))

        Description = descriptionParagraph + descriptionListing
        Description = Description.replace("  ","").decode("utf_8")
        item['Description'] = Description


        otherInfo = response.selector.xpath("//ul[@class='normal-list reduced-spacing-list']/li").extract()
        otherInfo = str(otherInfo)
        otherInfo = otherInfo.replace("<strong>","").replace("</strong>","").replace("<li>","").replace("</li>","").replace("  ","").replace("\\t","").replace("[","").replace("u'","").replace("]","").replace("\\n","").replace("'","").decode("utf_8")
        # for li in otherInfo:
        #     print str(li.replace("<strong>","").replace("</strong>","").replace("<li>","").replace("</li>","").replace("  ",""))
        item['OtherInfo'] = otherInfo


        imagesURLS = []

        Mainpicture = response.selector.xpath("//div[@id='Hero']/img/@src").extract()
        Mainpicture = Mainpicture.pop(0)
        # Mainpicture = str(Mainpicture)
        # Mainpicture = Mainpicture.replace("u'","").replace("[","").replace("]","").replace("'","").strip()
        Mainpicture = Mainpicture.strip()
        imagesURLS.append(Mainpicture)

        pictures = response.selector.xpath("//ul[@class='component-carousel-qinfo component-carousel-6 carousel6Width']/li/a/img/@src").extract()
        for picture in pictures:
            tempPicUrl = picture.replace('wid=60','wid=480').replace('hei=60','hei=480')
            # picture = str(picture)
            # picture = picture.replace("u'","").replace("[","").replace("]","").replace("'","").replace("60","480").strip()
            # #Index = picture.index("wid=")
            # #Extrapicture = picture[]
            imagesURLS.append(tempPicUrl)

        # for i in imagesURLS:

            # print "#############" + i


        ALLpicture = list(set(imagesURLS))
        item['image_urls'] = [ img for img in ALLpicture ]


        #print "######################################" + picture

        return item

