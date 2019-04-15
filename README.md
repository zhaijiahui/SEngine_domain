# SEngine_domain

通过搜索引擎收集域名信息

collect domain name from search engine

如果使用-o参数进行保存结果，请在python3.x环境下使用

if you want to save result use -o option , and please run in python3.x



# Change Log

[+][2018-09-03] 	初始功能，添加说明信息

[+][2018-10-17] 	添加README说明

[+][2019-1-6] 	BUG#1  修改浏览器高级搜索

[+][2019-4-15] 	BUG#2  baidu 模块优化，调整编码问题



# Dependencies

pip install requests lxml beautifulsoup4




# Usage


### Collect subdomains through search engines by zhaijiahui


-k  Input your keyword

-p  Page number

-o  Save result to csv

-s  Prevent requests too fast

   Support Search Engines: baidu,bing,so360,sogou(default)
​    
   Yahoo(slow!)
   				
   Usage: engine2.py -k yourkeywords -p 10 -o
​	
​	
# keywords example:

maybe USELIST.txt can help you.....

- 1.engine2.py -k 腾讯 -p 1

- 2.engine2.py -k inurl:qq.com -p 2

- 3.engine2.py -k intext:微信 -p 3 -o

- 4.engine2.py -k site:Github.com -p 2

- 5.and many more...
