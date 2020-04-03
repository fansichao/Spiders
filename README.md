# Spider

环境说明
- `Python3.6`
- `Centos7.5`
- `Scrapy框架` & `简单py爬虫`

TODO

- 代理IP
- 百度网盘 提取码的自动转存问题
- 大圣盘IP被锁问题

## Project

- Baiduyun 
    - 查询 盘搜搜 上百度云盘资源
    - 将云盘资源保存到百度网盘中
- MockPLus
    - 自动获取 MockPlus 精美模板

## 常用命令


```python
# 
scrapy startproject baidu
# 传递参数
# scrapy crawl pansoso1 -a search_text=excel
# TODO 直接搜索百度API
```

## 百度网盘网站资源说明

通用参数说明:

- mode 保存模式 append/override 
- search_text 搜索内容
- page 搜索页数

### 盘搜搜

网站资源一般,链接存在加密,存在访问过多时IP封锁.

网站链接: 网盘资源 www.pansoso.com


```python
# 项目命令
scrapy crawl pansoso01 -a search_text=excel
scrapy crawl pansoso02
scrapy crawl pansoso03
```

### 大圣盘(建议)

说明:

- 大多资源有效,且网站存在资源校验机制. 
- 资源分为无提取码和有提取码两种.
- 资源文件都较大,且命名不规范,或非实际所需文件
- 反爬虫机制
    - 延迟加载(提取码 & 提取码是否有效)
        - 解决方法: 使用selenium(浏览器处理)

网站链接: 网盘资源 www.dashengpan.com

```python
# 项目命令
scrapy crawl dashengpan01 -a mode=append -a search_text=excel -a page=1
```

### 搜百度盘

说明:

- 搜百度盘 网站简单,适合练手
- 但是资源基本(99%)都是无效资源,无过多反爬虫机制.
- 不建议使用此网站

```python
# 项目命令
scrapy crawl sobaidupan01 -a search_text=excel  -a page=1000
scrapy crawl sobaidupan02
```

网站链接: 网盘资源 www.sobaidupan.com


## 附件

### 使用样例

```python
# 爬取百度网盘资源
1. scrapy crawl dashengpan01 -a mode=append -a search_text="app inventor" -a page=5 
2. scrapy crawl dashengpan02 # 必须在图形化界面打开

# 将网盘资源保存到百度网盘
python baiduyun_tools.py -filename xxxxx -cookie xxxxx -path xxxx

# 输出说明
success.txt 记录成功运行的 URL, 下次运行时不会在运行此中URL

```

### 参考链接

- [自动将资源添加到百度网盘中](https://github.com/tengzhangchao/BaiDuPan)
- [Scrapy_延迟加载](https://zhuanlan.zhihu.com/p/72887277)


免责说明:

1. 非商业用途.
2. 如有侵犯您的合法权益或违法违规，请提供相关有效书面证明与侵权页面链接联系我们进行删除。感谢您的支持




