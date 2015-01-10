#coding=utf-8
import urllib2
import httplib
import json
import re
import codecs
import os
		

def writeToFile(file_obj,record):
	file_obj.write("usr_id:")
	file_obj.write(str(record["id"]))
	file_obj.write("\n")

	file_obj.write("hasPicture:")
	if record["pics"] == "":
		file_obj.write("N")
	else:
		file_obj.write("Y")
	file_obj.write("\n")
	file_obj.write("hasAppendComment:")
	if record["appendComment"] == "":
		file_obj.write("N")
	else:
		file_obj.write("Y")
	file_obj.write("\n")
	file_obj.write("tmallRate:")
	file_obj.write(str(record["tamllSweetLevel"]))
	file_obj.write("\n")
	file_obj.write("userLevel:")
	file_obj.write(record["displayRatePic"])
	file_obj.write("\n")
	file_obj.write("productType:")
	file_obj.write(record["auctionSku"])
	file_obj.write("\n")
	file_obj.write("content:")
	file_obj.write(record["rateContent"])
	file_obj.write('\n\n')

def fromShopToURL(shopurl):
	response = urllib2.urlopen(shopurl)
	body = response.read()
	print body

def getcomment(comment_url):
	for page in range(1,400):
		print page
		x1 = u"/list_detail_rate.htm?.*currentPage="
		pat1 = re.compile(x1)
		url1 = pat1.findall(comment_url)
		print url1[0]
		
		x2 = u"&append=.*"
		pat2 = re.compile(x2)
		url2 = pat2.findall(comment_url)
		print url2[0]
		
		url = url1[0] + str(page) + url2[0]
		jsongetter(url)

lastlength = 0
def jsongetter(url):
	global lastlength
	conn = httplib.HTTPConnection('rate.tmall.com')
	conn.request('GET',url)
	res = conn.getresponse()
	try:
		body =  res.read().decode('gbk').encode('utf-8')
	except UnicodeDecodeError,e:
		print e
		return
	if len(body) == lastlength:
		os._exit(0)
	else:
		lastlength = len(body)

	xx = u"\[.*\]"
	patt = re.compile(xx)
	result = patt.findall(body)
	file_obj = codecs.open('data.txt','a+',"utf-8")
	for js in result:
		data = json.loads(js)
		for record in data:
			writeToFile(file_obj,record)
		#	print record
		#	print "\n"
	file_obj.close()


#main:
comment_url = "http://rate.tmall.com/list_detail_rate.htm?itemId=39931561567&spuId=282819001&sellerId=1114511827&order=1&currentPage=1&append=0&content=1&tagId=&posi=&picture=&ua=220UW5TcyMNYQwiAiwZTXFIdUh1SHJOe0BuOG4%3D%7CUm5Ockt0SXxIdkJ9RXlAeS8%3D%7CU2xMHDJ7G2AHYg8hAS8RJQsrBUIrQG44bg%3D%3D%7CVGhXd1llXGNea19hVWpSblduWWRGf0tzR39DfUZ7QXVIdU14THZYDg%3D%3D%7CVWldfS0RMQQkGjoUOBxxXwlf%7CVmhIGCcZOQQkGCcSLw8xCz8CIh4hFCkJPAE8HCAfKhc3DTAEUgQ%3D%7CV25OHjAePgcyCioWLxYvDzYKMwlfCQ%3D%3D%7CWGBAED4QMGBZbVJyTndIfFxlW2JCdk9tV2NYbVdvT3NMeVllXAoqFzcZNxcuGiccShw%3D%7CWWBdYEB9XWJCfkd7W2VdZ0d%2BXmJff0N2IA%3D%3D&_ksTS=1420893930333_1075&callback=jsonp1076"
getcomment(comment_url)