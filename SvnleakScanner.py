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

ipfile ='url.txt'
exitFlag = 0
wr = open("./result.txt",'w+')
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

def check_svn(url):
    html = ''
    try:
        urlsvn = url+"/.svn/entries"
        opener = urllib2.build_opener(RedirectHandler)
        response = opener.open(urlsvn,timeout=4)
        try:
            html = response.read()
            html = json.loads(html)
            pass
        except:
            if (html and "svn:" in html) or ("dir" in html and "DoCTYPE" not in html and "DOCTYPE" not in html and "<script" not in html and "html>" not in html and "doctype" not in html and "Active connections" not in html and html !="([]);" and len(html.strip())>0):
                return urlsvn
    except Exception, e:
    	return "error"
        pass
    return "error"


def check_git(url):
    html = ''
    try:
        urlgit = url+"/.git/config"
        opener = urllib2.build_opener(RedirectHandler)
        response = opener.open(urlgit,timeout=4)
        try:
            html = response.read()
            html = json.loads(html)
            pass
        except:
            if (html and "core" in html) or ("origin" in html and "DoCTYPE" not in html and "DOCTYPE" not in html and "<script" not in html and "html>" not in html and "doctype" not in html and "Active connections" not in html and html !="([]);" and len(html.strip())>0):
                return urlgit
    except Exception, e:
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
				csvn = check_svn("http://"+domain)
				
				if(csvn!="error"):
					print csvn + "  is exist"
					wr.write(csvn+"\n")
					result.append(csvn+"\n")
				
				cgit = check_git("http://" + domain)
				
				if(cgit!="error"):
					print cgit + "  is exist"
					wr.write(cgit+"\n")
					result.append(cgit+"\n")
				
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