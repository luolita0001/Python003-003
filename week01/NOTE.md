# WEEK1 知识总结

# 一.scrapy简单介绍

<font color=#999AAA >scrapy是爬虫的框架，使用scrapy可以编写高效的大型爬虫，安装方法可以通过pip install scrapy来进行安装。</font>

<hr style=" border:solid; width:100px; height:1px;" color=#000000 size=1">


## 1.scrapy框架结构解析

scrapy有7项核心组件，我们需要了解他们的功能和运行流程。

**引擎**（Engine）：是scrapy的“大脑”，帮助我们高效爬取并行处理数据的。
**调度器**（Scheduler）:调度器接受引擎发过来的请求，按照先后顺序，压入列队中，同时去除重复的请求。
**下载器**（Downloader）：下载器用于下载网页内容，并返回给爬虫，就是scrapy中的Request组件。
**爬虫**（Spiders）：用于从特定的网页中提取需要的信息，对提取出的链接，可以发起下一次请求。
**项目**（Item Pipelines）:项目管道负责处理爬虫从网页中抽取出的实体，并且保存成文件或存入数据库中。
另外还有**下载器中间件**(Downloader Middlewares)和 **爬虫中间体**（Spider Middlewares )就不过多介绍了，详情可以查看官网链接。




 - scrapy运行流程解析

其中Spiders和pipeline 是需要我们去修改的，其他组件无需修改，框架已写好
![scrapy组件运行流程](https://img-blog.csdnimg.cn/20200822214734501.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2x1b2xpdGEwMDE=,size_16,color_FFFFFF,t_70#pic_center)

 1. 首先，引擎根据我们填写的域名（例如，要爬取豆瓣，则域名为 douban.com ）找到相应的Sipders组件，然后Spiders组会对爬取的url进行发送请求，发起的信息由绿色的线先后传入到调度器，并在调度器中进行去重操作。
 2. 并根据请求的传入顺序，Scheduler会将请求再发给引擎，再由引擎发送给下载器。其中Downloader相当于requests方法，对网页真正发起请求，请求过后不论成功失败都有一个返回，也由Downloader接受返回信息。（Downloader Middlewares）是一个下载中间件，可以起到一个过滤的作用。
 3. 返回后的数据交给引擎再交给Spiders.
 4. Spiders后有两个方向，其中一个是items最终传入的是Item Pipeline,对返回数据对实体化操作，进行文件保存等。
 5. 第二个是Requests，其中反映了框架的优势，不需要再次编写requests的条件。


## 2. scrapy爬虫目录结构解析
1. 打开终端，再当前目录下创建了名为quotes的quotes项目`$ scrapy startproject quotes`
2. 并且根据提示进入quotes文件夹内 `$ cd quotes` 
3. 再进入spiders文件夹内 `$cd spiders`
4. 创建quote_css.py 爬虫，`$ scrapy genspider quote_css "quotes.toscrape.com"`，其中"quotes.toscrape.com"为要爬取的网页的域名，例如，豆瓣的域名为"douban.com"，会影响scrapy里的基本设置，最好根据需要填写。（注意：一个项目里可以包含多个Spiders，例如 `$ scrapy genspider quote_xpath "quotes.toscrape.com"`再同一个项目内创建了quote_xpath.py爬虫。

![创建好后的目录结构](https://img-blog.csdnimg.cn/20200822223613146.png#pic_center)
5.调用爬虫,scrapy框架书写的爬虫，不能直接运行，需要在终端，在quotes/quotes 目录下 `$scrapy crawl quote_css`运行。
6.将返回内容保存为json文件，同样也需要在quotes/quotes 目录下 `$ scrapy crawl quote_xpath -o quotes.json`