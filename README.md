#爬虫整体流程思路：
* 目标网站
	* 准备url
		- 页码总数明确
			~ 构建url地址
		- 页码总数不明确
			~ 通过代码提取下一页

	- 发送请求，获取响应
		- 网站无反爬
			###### 直接获取响应信息
		- 网站有反爬
			###### 添加请求头， 代理ip，cooklie
			- 如果不登录
				###### 维护cooklie会话 可以用session来解决
			- 如果要登录
				###### 准备多个帐号，维护一个cookie池 ，随机选择cookie登录

	- 提取数据
		- 数据在页面里
			- 提取内容
				###### BeautifulSoup 解析网页神器，可以专门用来解析html
				###### PyQuery   强大的网页解析库，是python仿照JQuery实现
				###### lxml     高性能的Python HTML/XML解析器
				###### 正则表达式      提取信息
		- 数据不在页面里
			###### 使用浏览器开发者工具F12， Fidler， Charles等抓包
			###### 查找数据的位置，提取构建url

	- 保存数据
		- 保存到本地
			###### text, json, csv
		- 保存到数据库
			###### Mysql  关系型数据库
			###### MongoDB    文档型数据库
			###### Redis      键值存储数据库

## 进阶操作：
- scrapy 异步爬虫框架
    - 优点 
        - 异步
        - 支持shell调试
    - 缺点
        - 本身不支持分布式，因为scrapy中的调度器是运行在队列中，而队列是在单机内存中，所以服务器上的爬虫无法利用内存的队列进行处理
- scrapy-redis分布式
    - 可以配合 redis使用分布式
        - 原理是 Scrapy的调度器、去重器&emsp;和&emsp;redis的进行替换，抓取的任务就会加入到一个表中，这样就可以进行任务共享操作
- 最后还可以用pandas， matplotlib 数据可视化，numpy进行数据分析

### 反爬
- 封ip，封User-gent
- 验证码，cookie验证
- JaveScript渲染
- Ajax异步加载
- 字体反爬
- 使用算法加密
- robots协议   





