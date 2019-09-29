# 分布式爬虫
- 简单说白了就是，在不同的机器上执行配置一样的爬虫项目，只不过获取的url
  存在了redis数据库里，并在redis执行去重，抓取操作。
## redis分布式部署
```python
#在scrapy中settings 添加：
  
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter" #配置scrapy使用的去重类，RFPDupeFilter
SCHEDULER = "scrapy_redis.scheduler.Scheduler"  #redis的调度器
SCHEDULER_PERSIST = True  # 调度器数据持久化
REDIS_URL = "redis://172.168.70.171:6379"  #redis主机的配置信息

并且添加：
ITEM_PIPELINES ={
 'scrapy_redis.pipelines.RedisPipeline':1
}

#在爬虫里面
导入 from scrapy_redis.spiders import RedisSpider
并把 (scrapy.Spider)改为(RedisSpider)
注释start_urls = 'http://..........'
添加 redis_key = '爬虫名：start_urls'  
```

### 部署完毕之后，启动项目
```text
1.在各个分机上开启爬虫项目

2.在主机上开启redis(以下为windows10举例):

redis-server.exe redis.windows.conf

远程连接
redis-cli.exe -h 192.168.0.103 -p 6379

添加爬取url
lpush 爬虫名字:start_url 爬取的http地址


```

