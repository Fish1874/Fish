# 热爱互联网行业，希望能在工作中学到更多東西，提升自身！
## 爬虫整体流程思路：
- 准备url
- 目标网站
    - 页码总数明确
        ~ 构建url地址
    - 页码总数不明确
        ~ 通过代码提取下一页

- 发送请求，获取响应
    - 网站无反爬
        - 直接获取响应信息
    - 网站有反爬
        - [封ip，封User-gent](https://github.com/Fish1874/Fish/blob/master/%E5%B0%8F%E7%88%AC%E8%99%AB/%E6%8B%89%E5%8B%BE%E7%BD%91%E5%8F%8D%E7%88%AC.py)
        - [验证码](https://github.com/Fish1874/knowledge/tree/master/python/yundama)
        - [cookie验证](https://github.com/Fish1874/Fish/blob/master/%E5%B0%8F%E7%88%AC%E8%99%AB/crawler-basic-1.py)
        - [JaveScript渲染](https://github.com/Fish1874/Fish/tree/master/JS%E9%80%86%E5%90%91%E7%88%AC%E8%99%AB)
        - [Ajax异步加载](https://github.com/Fish1874/Fish/blob/master/%E5%B0%8F%E7%88%AC%E8%99%AB/Ajax%E5%8F%8D%E7%88%AC.py)
        - 字体反爬
        - 使用算法加密
    - 如果不登录
        - 维护cooklie会话 可以用session来解决
    - 如果要登录
        - 准备多个帐号，维护一个cookie池 ，随机选择cookie登录

- 提取数据
    - 数据在页面里
        - 提取内容
            - [正则表达式](https://github.com/Fish1874/Fish/blob/master/%E5%B0%8F%E7%88%AC%E8%99%AB/%E6%AD%A3%E5%88%99%E8%A1%A8%E8%BE%BE%E5%BC%8F%E7%88%AC%E5%8F%96%E5%86%85%E5%AE%B9.py)  
            强大的文本操作
            - [lxml](https://github.com/Fish1874/Fish/blob/master/%E5%B0%8F%E7%88%AC%E8%99%AB/Xpath%E7%88%AC%E5%8F%96%E7%94%B5%E5%BD%B1%E5%A4%A9%E5%A0%82.py)  
            高性能的Python HTML/XML解析器
            - [pyquery](https://github.com/Fish1874/Fish/blob/master/%E5%B0%8F%E7%88%AC%E8%99%AB/bokeyuan.py)
            仿照jQuery的网页解析库
            - [BeautifulSoup](https://github.com/Fish1874/Fish/blob/master/%E5%B0%8F%E7%88%AC%E8%99%AB/douban/douban/spiders/doubanmovie.py)
            解析网页神器，可以专门用来解析html



- 数据不在页面里
    ###### 使用浏览器开发者工具F12， Fidler， Charles等抓包
    ###### 查找数据的位置，提取构建url

- 保存数据
    - [保存到本地](https://github.com/Fish1874/Fish/blob/master/%E5%B0%8F%E7%88%AC%E8%99%AB/%E7%B3%97%E4%BA%8B%E7%99%BE%E7%A7%91.py)
        ###### text, json, csv
    - 保存到数据库
        ###### [Mysql  关系型数据库](https://github.com/Fish1874/knowledge/blob/master/%E6%95%B0%E6%8D%AE%E5%BA%93/pymysql.md)
        ###### [MongoDB文档型数据库](https://github.com/Fish1874/knowledge/blob/master/%E6%95%B0%E6%8D%AE%E5%BA%93/mongodb.md)
        ###### Redis      键值存储数据库

## 进阶操作：
- [scrapy 异步爬虫框架](https://github.com/Fish1874/knowledge/blob/master/python/scrapy%E7%9F%A5%E8%AF%86%E7%82%B9.md)
    - 优点 
        - [异步](https://github.com/Fish1874/knowledge/blob/master/python/%E5%BC%82%E6%AD%A5%E5%8D%8F%E7%A8%8B.md)
        - 支持shell调试
    - 缺点
        - 本身不支持分布式，因为scrapy中的调度器是运行在队列中，而队列是在单机内存中，所以服务器上的爬虫无法利用内存的队列进行处理
- [scrapy-redis分布式]()
    - 可以配合 redis使用分布式
        - 原理是 Scrapy的调度器、去重器&emsp;和&emsp;redis的进行替换，抓取的任务就会加入到redis数据库中，这样就可以进行任务共享操作
- 最后还可以用pandas， matplotlib 数据可视化，numpy进行数据分析








