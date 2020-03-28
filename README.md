# Spider

环境说明
- `Python3.6`
- `Centos7.5`
- `Scrapy框架` & `简单py爬虫`

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

网站链接: 网盘资源 www.dashengpan.com

```python
# 项目命令
scrapy crawl dashengpan01 -a mode=override -a search_text=excel -a page=1

scrapy crawl pansoso01 -a search_text=excel
scrapy crawl pansoso02
scrapy crawl pansoso03
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


## 参考链接

- [自动将资源添加到百度网盘中](https://github.com/tengzhangchao/BaiDuPan)

