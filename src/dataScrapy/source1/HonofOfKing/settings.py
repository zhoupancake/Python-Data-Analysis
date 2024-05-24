BOT_NAME = 'HonofOfKing'

SPIDER_MODULES = ['HonofOfKing.spiders']
NEWSPIDER_MODULE = 'HonofOfKing.spiders'

ROBOTSTXT_OBEY = False

DOWNLOAD_DELAY = 3

COOKIES_ENABLED = True

DEFAULT_REQUEST_HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Language': 'en',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
    'Referer': "http://db.18183.com/wzry/hero/16327.html",
    'Cookie': "UM_distinctid=174bdbead477a7-0dc690e6349815-333376b-1fa400-174bdbead48c2f; Hm_lvt_3782151c2b39bc6837a4913c89752cbc=1610805654,1610854292; CNZZDATA30081741=cnzz_eid%3D575897274-1610800770-%26ntime%3D1610887731; CNZZDATA30070880=cnzz_eid%3D1270013658-1610803142-%26ntime%3D1610888319; CNZZDATA1255763238=209075917-1610803462-%7C1610888285; CNZZDATA1260805952=1325796982-1610801701-%7C1610890050; Hm_lpvt_3782151c2b39bc6837a4913c89752cbc=1610891869"
}

ITEM_PIPELINES = {
   'HonofOfKing.pipelines.HonofofkingPipeline': 300,
}