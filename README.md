# SEngine_domain

通过搜索引擎收集域名信息
collect domain name from search engine
如果使用-o参数进行保存结果，请在python3.x环境下使用
if you wang to save result,please run in python3.x


# Change Log

[+][2018-09-03] 初始功能，添加说明信息

# Dependencies

pip install requests lxml beautifulsoup4


# Usage


### Collect subdomains through search engines by zhaijiahui


-k  Input your keyword

-p  Page number

-o  Save result to csv

-s  Prevent requests too fast

   Support Search Engines: baidu,bing,so360,sogou(default)
    
   Yahoo(slow!)
   				
   Usage: engine2.py -k yourkeywords -p 10 -o
	
	
# yourkeywords example:



1.engine2.py -k 腾讯 -p 1

2.engine2.py -k site:qq.com -p 2

3.engine2.py -k intext:微信 -p 3 -o

4.and many more...
