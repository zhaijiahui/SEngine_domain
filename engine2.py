# -*- coding:utf-8 -*-
import requests,re
from bs4 import BeautifulSoup
import getopt,sys,os,time
import socket
import csv
import io  
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')         #改变标准输出的默认编码  

remove_list = ['sowang','sogou','baidu','sina','so','jd','tianyancha','qq','zhihu','finance','eastmoney','360'\
,'ifeng','gaokaopai','chinaz','163'] # Exclude interference domain
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
	
	for i in range(0,page):
		print('[+]	Baidu search '+str(i+1)+' page...')
		url = 'https://www.baidu.com/s?wd='+keywords+'&pn='+str(i*10)
		print(url)
		r = requests.get(url,headers=header)
		html = r.content.decode('utf-8')
		# print(html)
		soup = BeautifulSoup(html,'lxml')
		f13 = soup.find_all("div",class_="f13")

		for span in f13:
			showurl = span.find("a",class_="c-showurl")
			try:
				surl = showurl.string
				relpa = ['<b>','</b>','/\xa0']
				for i in relpa:
					surl = surl.replace(i,'')
				# surl = surl[0].replace('<b>','').replace('</b>/\xa0','')
				# print(surl)
				if surl.split('.')[1] not in remove_list:
					domain_list.append(surl.strip())
					# domain_list.append('/'.join(domain[:3]))
			except Exception as e:
				pass
			
	# domain_list = list(set(domain_list))
	return domain_list

def bing_engine(keywords,page):
	domain_list = []
	if 'inurl' in keywords:
		keywords = keywords.replace('inurl','site')
	for i in range(0,page):
		print('[+]	Bing search '+str(i+1)+' page...')
		if i == 0:
			url = 'https://cn.bing.com/search?q='+keywords+'&FORM=PERE&first=1'
		else:
			url = 'https://cn.bing.com/search?q='+keywords+'&FORM=PERE'+str(i)+'&first='+str(i*10)
		header['Cookie'] = 'DUP=Q=Zoz3W9SS4tU-JWtehzNXtQ2&T=347468387&A=2&IG=A33678F9B7304F81A900C45AA2A1B940; _EDGE_V=1; MUID=16D4CEBA7E0E6B7B2F32C5257FB96A1D; MUIDB=16D4CEBA7E0E6B7B2F32C5257FB96A1D; SRCHD=AF=NOFORM; SRCHUID=V=2&GUID=9DE844CCC2984C9D960C37BDEF3FB4D3&dmnchg=1; _EDGE_S=mkt=zh-cn&SID=33BA6C198AEA6ABA2C2F60C38BD66B58; ULC=P=28B3|5:@4&H=28B3|16:13&T=28B3|16:13; _FP=hta=on; ENSEARCH=TIPBUBBLE=1&BENVER=0; SRCHUSR=DOB=20180223&T=1546651874000; _SS=SID=33BA6C198AEA6ABA2C2F60C38BD66B58&bIm=211444&HV=1546651874; ipv6=hit=1546655475143&t=4; SRCHHPGUSR=CW=1501&CH=402&DPR=1.25&UTC=480&WTS=63682248674'
		print(url)
		r = requests.get(url,headers=header)
		html = r.content.decode('utf-8')
		# soup = BeautifulSoup(html,'lxml')
		# print(html)
		href = re.findall('<a target="_blank" href="(.+?)" h="ID=SERP',html)
		# print(href)
		# for x in soup.find_all('a',):
		# 	print(x.string)
		for x in href:
			if x.split('.')[1] not in remove_list:
				domain_list.append(x.split('/')[2])
	# domain_list = list(set(domain_list))
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
					domain_list.append(temp.strip())
	# domain_list = list(set(domain_list))
	return domain_list

def so360_engine(keywords,page):
	domain_list = []
	if 'inurl' in keywords:
		keywords = keywords.replace('inurl','site')
	for i in range(1,page+1):
		url = 'https://www.so.com/s?q='+keywords+'&pn=' + str(i)
		print('[+]	so360 search '+str(i)+' page...')
		print(url)
		r = requests.get(url,headers=header)
		html = r.content.decode('utf-8')
		soup = BeautifulSoup(html,'lxml')

		for i in soup.find_all("a",class_="mingpian"):
			link = i.get('data-h')
			# print(link)
			if link.split('.')[1] not in remove_list:
				domain_list.append(link.strip())
	# domain_list = list(set(domain_list))
	return domain_list

def sogou_engine(keywords,page):
	domain_list = []
	for i in range(1,page+1):
		url = 'https://www.sogou.com/web?query='+keywords+'&page=' + str(i)+'&ie=utf8'
		print('[+]	Sogou search '+str(i)+' page...')
		r = requests.get(url,headers=header)
		html = r.content.decode('utf-8')
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
					domain_list.append(link.strip())
	# domain_list = list(set(domain_list))
	return domain_list


def main():
	writefile = False
	Usage='''
# ------------------------------------------------------------
# Collect subdomains through search engines by zhaijiahui
# ------------------------------------------------------------\n
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
	print(baidu_list)
	bing_list = bing_engine(keywords,page)
	print(bing_list)
	# Yagoo_list = Yahoo_engine(keywords,page)
	so360_list = so360_engine(keywords,page)
	print(so360_list)
	sogou_list = sogou_engine(keywords,page)
	print(sogou_list)
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
				print(x+'	'+' '.join(get_ip_list(x))) # output domain and ip
				writer.writerow([x,' '.join(get_ip_list(x))])
				# print(x) # just output domain
		print('+-------------------save---------------------+')
		print('save to: '+ os.getcwd() + os.sep + writename)
		csvfile.close()
	else:
		for x in result_list:
			print(x+'	'+' '.join(get_ip_list(x))) # output domain and ip
			# print(x) # just output domain


if __name__ == '__main__':
	main()