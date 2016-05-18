#!python
#-*- coding:utf8 -*-
# author			: glacier@insight-labs.org
# version			: v1.0

import Queue
import threading
import socket
import time
import urllib2

ipfile ='ips.txt'
exitFlag = 0
wr = open("./result.txt",'a')
result = []
timeout = 5
threadnum = 200
socket.setdefaulttimeout(timeout)  #设置了全局默认超时时间
urllib2.socket.setdefaulttimeout(timeout) 


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

def verify_vul(url):
    html = ''
    #url = url#+"/containers/json"
    try:
        
        opener = urllib2.build_opener(RedirectHandler)
        response = opener.open(url,timeout=timeout)
        html = response.read()
    except urllib2.HTTPError,e:
        if(e.code==404):
           return urlsvn  
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
				docker = verify_vul("http://"+domain+":2375")
				
				if(docker!="error"):
					print docker + "  is exist"
					wr.write(docker+"\n")
					result.append(docker+"\n")
	q.task_done()

queueLock = threading.Lock()
workQueue = Queue.Queue(10)
threads = []
tid = 0
# 创建新线程
for i in range(threadnum):
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