BOT_NAME = 'spider_steam'

SPIDER_MODULES = ['spider_steam.spiders']
NEWSPIDER_MODULE = 'spider_steam.spiders'


ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
   'spider_steam.pipelines.SpiderSteamPipeline': 300,
}

REQUEST_FINGERPRINTER_IMPLEMENTATION = '2.7'
TWISTED_REACTOR = 'twisted.internet.asyncioreactor.AsyncioSelectorReactor'
