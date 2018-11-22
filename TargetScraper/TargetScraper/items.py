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


