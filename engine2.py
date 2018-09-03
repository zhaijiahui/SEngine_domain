# -*- coding:utf-8 -*-
import requests,re
from bs4 import BeautifulSoup
import getopt,sys,os,time
import socket
import csv

remove_list = ['sowang','sogou','baidu','sina','so','jd','tianyancha','qq','zhihu','finance','eastmoney','360'\
,'ifeng','gaokaopai'] # Exclude interference domain
header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36'}


def get_ip_list(domain):  # Parsing the IP list
    ip_list = []
    try:
        addrs = socket.getaddrinfo(domain, None)
        for item in addrs:
            if item[4][0] not in ip_list:
                ip_list.append(item[4][0])
    except Exception as e:
        # print(str(e))
        pass
    return ip_list

def baidu_engine(keywords,page):
	domain_list = []
	for i in range(page):
		url = 'https://www.baidu.com/s?wd='+keywords+'&pn='+str(i*10)
		print('[+]	Baidu search '+str(i)+' page...')
		r = requests.get(url,headers=header)
		html = r.content.decode('utf-8')
		soup = BeautifulSoup(html,'lxml')
		content_left = soup.find("div",id="content_left")
		for span in content_left.find_all("a",class_="c-showurl"):
			url = span.string
			# a_url = span.get('href')
			# print(url)
			if url:
				domain = url.split('/')
				# print(domain)
				for i in domain:
					if '.' in i:
						if '...' not in i:
							if i.split('.')[1] not in remove_list:
								domain_list.append(i)
								# domain_list.append('/'.join(domain[:3]))
	domain_list = list(set(domain_list))
	return domain_list

def bing_engine(keywords,page):
	domain_list = []
	for i in range(0,page):
		if i == 0:
			url = 'https://cn.bing.com/search?q='+keywords+'&FORM=PERE&first=1'
		else:
			url = 'https://cn.bing.com/search?q='+keywords+'&FORM=PERE'+str(i)+'&first='+str(i*10)
		print('[+]	Bing search '+str(i)+' page...')
		header['Cookie'] = '_EDGE_V=1; MUID=16D4CEBA7E0E6B7B2F32C5257FB96A1D; MUIDB=16D4CEBA7E0E6B7B2F32C5257FB96A1D; SRCHD=AF=NOFORM; SRCHUID=V=2&GUID=9DE844CCC2984C9D960C37BDEF3FB4D3&dmnchg=1; BFBN=gRCpIwEkh3vZLcugIKnHADUzLERsJGiQ_BrNBV31m2HAeg; ULC=P=13AEA|1:@1&H=13AEA|12:10&T=13AEA|12:10; ENSEARCH=TIPBUBBLE=1&BENVER=0; ipv6=hit=1533606783456&t=4; _EDGE_S=mkt=zh-cn&SID=365BCAC7E54064700BE2C683E46E65E1; SRCHUSR=DOB=20180223&T=1533603962000; _FP=hta=on; _SS=SID=365BCAC7E54064700BE2C683E46E65E1&bIm=562316&HV=1533604112; SRCHHPGUSR=CW=1519&CH=150&DPR=1.25&UTC=480&WTS=63669199983'

		r = requests.get(url,headers=header)
		html = r.content.decode('utf-8')
		soup = BeautifulSoup(html,'lxml')
		
		for x in soup.find_all('cite'):
			if x.string:
				if x.string != '必应本地':
					# print(x.string)
					if 'https://' in x.string:
						temp = x.string.replace('https://','')
					else:
						temp = x.string
					# print(temp)
					if '/' in temp:
						temp = temp.split('/')[0].split('.')[1]
					else:
						temp = temp.split('.')[1]
					
					if temp not in remove_list:
						domain_list.append(x.string)
	domain_list = list(set(domain_list))
	return domain_list

def Yahoo_engine(keywords,page):
	domain_list = []
	for i in range(page):
		url = 'https://sg.search.yahoo.com/search?fr2=sa-gp-sg.search&p='+keywords+'&fr=sfp&iscqry=&pz=10&b='+str(i*10+1)
		print('[+]	Yahoo search '+str(i)+' page...')
		r = requests.get(url,headers=header)
		html = r.content.decode('utf-8')
		soup = BeautifulSoup(html,'lxml')
		for i in soup.find_all('span',class_=' fz-ms fw-m fc-12th wr-bw lh-17'):
			temp = i.string
			if temp:
				if '/' in temp:
					kk = temp.split('/')[0].split('.')[1]
				else:
					kk = temp.split('.')[1]
				if kk not in remove_list:
					domain_list.append(temp)
	domain_list = list(set(domain_list))
	return domain_list

def so360_engine(keywords,page):
	domain_list = []
	for i in range(1,page):
		url = 'https://www.so.com/s?q='+keywords+'&pn=' + str(i)
		print('[+]	so360 search '+str(i)+' page...')
		r = requests.get(url,headers=header)
		html = r.content.decode('utf-8')
		# print(html)
		soup = BeautifulSoup(html,'lxml')

		for i in soup.find_all('cite'):
			# print(i.string)
			link = i.string
			if link:
				if '/' in link:
					link = link.split('/')[0]
				elif '>' in link:
					link = link.split('>')[0]
				# print(link)
				if link.split('.')[1] not in remove_list:
					domain_list.append(link)
	domain_list = list(set(domain_list))
	return domain_list

def sogou_engine(keywords,page):
	domain_list = []
	for i in range(1,page):
		url = 'https://www.sogou.com/web?query='+keywords+'&page=' + str(i)+'&ie=utf8'
		print('[+]	Sogou search '+str(i)+' page...')
		r = requests.get(url,headers=header)
		html = r.content.decode('utf-8')
		# print(html)
		domian = re.findall('<cite id="cacheresult_info_(.+?)">(.+?)<',html,re.S)
		for i in domian:
			if '&nbsp;-&nbsp;' in i[1]:
				string = i[1].split('&nbsp;-&nbsp;')[0]
			else:
				string = i[1]+keywords[5:]
			# print(string)
			if '-' in string:
				string = string.split('-')[1]
				# print(string)
				if '//' in string:
					string = string.split('//')[1]
				if '/' in string:
					link = string.split('/')[0]
				else:
					link = string
				# print(link.split('.')[-2])
				if link.split('.')[-2] not in remove_list:
					domain_list.append(link)
	domain_list = list(set(domain_list))
	return domain_list


def main():
	writefile = False
	Usage='''
# ------------------------------------------------------------
# Collect subdomains through search engines by zhaijiahui
# ------------------------------------------------------------
-k  Input your keyword
-p  Page number
-o  Save result to csv
-s  Prevent requests too fast
    Support Search Engines: baidu,bing,so360,sogou(default)
    						Yahoo(slow!)

    Usage: engine2.py -k yourkeywords -p 10 -o'''
	if not len(sys.argv[1:]):
		print(Usage)
		exit()
	try:
		options,args = getopt.getopt(sys.argv[1:],"hk:p:o",["help","keyword=","page=","outfile"])
	except getopt.GetoptError:
		exit()
	for option,value in options:
		if option in ("-h","--help"):
			print(Usage)
			exit()
		if option in ("-k","--keyword"):
			keywords = value
		if option in ("-p","--page"):
			page = int(value)
		# if option in ("-s","--sleep"):
		# 	sleep = int(value)
		if option in ("-o","--outfile"):
			writefile = True
	baidu_list = []
	bing_list = []
	result_list = []
	baidu_list = baidu_engine(keywords,page)
	bing_list = bing_engine(keywords,page)
	# Yagoo_list = Yahoo_engine(keywords,page)
	so360_list = so360_engine(keywords,page)
	sogou_list = sogou_engine(keywords,page)
	result_list.extend(baidu_list)
	result_list.extend(bing_list)
	# result_list.extend(Yagoo_list)
	result_list.extend(so360_list)
	result_list.extend(sogou_list)
	result_list = list(set(result_list))
	print('+-------------------result---------------------+')
	if writefile:
		if ":" in keywords:
			wname = keywords.split(":")[1]
		else:
			wname = keywords
		writename = wname+"_"+str(page)+"_"+str(int(time.time()))+".csv"
		with open(writename,"w+", newline='') as csvfile:
			writer = csv.writer(csvfile)
			writer.writerow(["Domain","Ip"])
			for x in result_list:
				print(x.strip()+'	'+' '.join(get_ip_list(x))) # output domain and ip
				writer.writerow([x,' '.join(get_ip_list(x))])
				# print(x) # just output domain
		print('+-------------------save---------------------+')
		print('save to: '+ os.getcwd() + os.sep + writename)
		csvfile.close()
	else:
		for x in result_list:
			print(x.strip()+'	'+' '.join(get_ip_list(x))) # output domain and ip
			# print(x) # just output domain


if __name__ == '__main__':
	main()