# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class TargetscraperItem(Item):
    Price = Field()
    Title = Field()
    Breadcrums = Field()
    Description = Field()
    OtherInfo = Field()
    image_urls = Field()
    images = Field()


class TargetmergedItem(Item):
    ItemNumbers = Field()


