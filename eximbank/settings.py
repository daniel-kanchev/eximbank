BOT_NAME = 'eximbank'
SPIDER_MODULES = ['eximbank.spiders']
NEWSPIDER_MODULE = 'eximbank.spiders'
ROBOTSTXT_OBEY = True
LOG_LEVEL = 'WARNING'
ITEM_PIPELINES = {
   'eximbank.pipelines.DatabasePipeline': 300,
}
