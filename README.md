# 政务数据爬虫

---

<h4 id="Contract">开头唠叨两句</h4>

在使用中有任何问题，可以反馈给我，以下联系方式跟我交流

* Author: Leo
* Wechat: Leo-sunhailin
* QQ: 379978424
* E-mail: 379978424@qq.com
* Github URL: [Github传送门](https://github.com/sunhailin-Leo/business_data_spider)

---

* 开发环境
    * 系统版本： Win10 x64
    * Python版本: Python 3.4.4
    * Python库版本详情:
        * flask: 0.12.2
        * Scrapy: 1.4.0
        * pymongo: 3.5.1
        * schedule: 0.5.0(暂时还在实验阶段)
    * 前端(Vue + elementUI):
        * 需要Node环境,开发环境是node 8.9.0
        * 前端项目的依赖在frontend里面的package.json中
            * 主要的一些依赖:
                * vue: 2.2.2
                * vue-router: 2.3.0
                * axios: 0.15.3
                * element-ui: 1.4.10
                * vuex: 2.0.0-rc.6
                * webpack: 2.2.1

---

* 安装方式

    * 爬虫和Flask
    ```Python
    # 在项目根目录运行安装
    pip install -r requirements.txt
    ```

    * 前端
    ```Shell
    # 在frontend目录下的是前端页面
    npm run dev
    ```

---

* 运行方式(后端Flask运行在8080端口,前端页面运行在9000端口)

    * 在根目录下的business_data_spider文件夹中(即和scarpy.cfg在同一路径下)
    * Windows下按住shift + 右键打开命令行, Linux 就cd 到那个路径下
    * 全量爬虫

```Python
scrapy crawlall

# 如果说有报错是 No module named 'win32api'的话,请执行如下命令:
pip install pypiwin32

```

* 单个爬虫

```Python
# 可以先使用以下命令查看当前有哪些爬虫
scrapy list

# 然后选择一个执行
scrapy crawl <你选择的爬虫名称>

```

* 增量爬虫

```Python
# 增量暂时有些问题 --- 需要爬取完全量的之后才有用
scrapy crawl spider_incremental
```

* Flask 查询接口

```Python
# 到backend的路径下. 后续会补充一个外部启动接口,不需要进入到项目根目录下
python spider_backend.py
```

* 前端页面Vue + elementUI(在frontend文件夹内)

```Shell
# 第一步安装依赖
npm install (网速一般可以使用cnpm.安装方法自行百度)

# 调试
npm run dev

# 打包
npm run build
```

---

<h3 id="issue">技术点、功能及一些注意事项</h3>

```Python

技术点:
    Scrapy(利用了CrawlProcess的线程模型进行多线程爬虫开发)
    MongoDB(监控模块Spider_Spy表设置了索引)

功能:
    1. 异步多线程获取所需要的政务数据(公司主体信息等等)
    2. 设计了监控模块(爬虫监控状态)
    3. 设置了LOG的输出到文件(但是不能同时输出到控制台和文件)
    4. 加入了Flask的接口层,可以调用接口进行查询,接口文档见下

注意事项:
    1. 所有关于时间戳的统统精确到毫秒级
       (秒级的话如果只有一页的时候,监控那张表的开始和结束时间会显示在同一秒内完)
    2. 目前监控模块全部已经实现

```

---

<h3 id="SpiderPlus">增量爬虫的想法与设计</h3>

功能: 存储数据的MD5的值,对数据进行对比

想法(或者叫方案):
 * Scrapy + Redis:
    * 问题: 实际上是不行的,因为数据并不是实时更新,不确定数据到底什么时候更新.需要持久化,而Redis是存在内存中的,当服务挂了或者电脑重启,数据就会丢失。
    * 解决办法: 只能设计一个比较长久的过期时间.但是如果服务挂了,或者电脑重启就只能重新进行全量爬虫。数据稳定性较差但是速度最快
 * Scrapy + MongoDB:
    * 问题: 数据量与原始数据的级别同量,在做增量的时候需要对数据库查询进行优化,设置索引,但是这样全量爬虫会增加数据库的IO负担.而且数据量级增加以后,对硬盘的占用空间更大.
    * 解决办法: 对字段设置索引以及慢查询优化

<strong>目前进度:</strong>

* 暂时使用第二种方法,设计MongoDB存储(完成于:2017-11-16)
* 已经初步将所有爬虫以及管道中新增的MD5数据存储的方法写好(完成于:2017-11-16)
* 存储和校验MD5模块已经编写完成.
    * 校验方面,由于有三个表的数据有些问题,暂时搁置一下(处罚信息没有唯一id去写入MD5表,不正常企业和企业年报存在单个id出现多次的数据)(完成于:2017-11-20)

---

<h3 id="future">未来开发的计划</h3>

<strong>"*" 代表重要程度(5个为最重要)</strong>

~~1. 将监控模块全覆盖~~

2. 增量爬虫的设计(*****) ---- 遇到严重的问题(解决了部分的增量爬虫)

3. 设计个通用爬虫,针对于本项目网站的政务数据(**)

4. 研究下Scrapy的日志系统,看看是否能够拆分每一个爬虫对应每一个日志(**)

~~5. 设计利用flask-restful + vue-admin做一个爬虫监控平台(***)~~

---

<h3 id="RestFulApi">接口文档</h3>


<h4>1. 监控状态列表</h4>

<h5>URI: `/v1/spider_list`</h5>

<h5>METHOD: `GET`</h5>

<h5>Authentication: 无</h5>

<strong>注：sid是任务ID号可以为空;pn是页码,不能为空;r是每页的条数,不能为空</strong>

Request:
```HTML

{
	"sid": "",
	"pn": 1
	"r": 6
}

```

Response:
```HTML

{
  "count": 6,
  "data": [
    {
      "spider_all_items": 131,
      "spider_createTime": 1510896834294,
      "spider_currPage": 1,
      "spider_endTime": 1510896834604,
      "spider_id": "e5e1c8ee-cb58-11e7-a088-f82819e1bcfa",
      "spider_name": "business_administrative_penalties",
      "spider_status": "ClosedOrFinished",
      "total_page": 1
    }
  ],
  "msg": "Success",
  "status": true
}

```

---

<h4>1. 查询</h4>

<h5>URI: `/v1/seaech`</h5>

<h5>METHOD: `GET`</h5>

<h5>Authentication: 无</h5>

<strong>注：name可以为空,返回全部;name不为空则返回具体的信息</strong>

Request:
```HTML
{
	"name": "business_shareholder_information"
}
```

Response:
```HTML

{
  "count": 6,
  "data": [
    {
      "spider_all_items": 1150073,
      "spider_createTime": 1510896836079,
      "spider_currPage": 116,
      "spider_endTime": 1510912460884,
      "spider_id": "e5e2174a-cb58-11e7-b48f-f82819e1bcfa",
      "spider_name": "business_shareholder_information",
      "spider_status": "ClosedOrFinished",
      "total_page": 116
    }
  ],
  "msg": "Success",
  "status": true
}

```
