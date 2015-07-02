#-*-coding:utf-8-*- 
import os,sys
import httplib
import string
import time
import urlparse 


def SendHTTPRequest(strMethod,strScheme,strHost,strURL,strParam):
    headers = {
        "Accept-Language": "zh-cn", 
        "Content-Type": "application/x-www-form-urlencoded", 
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)", 
        "Host": strHost,
        "Connection": "Keep-Alive", 
        "Cache-Control": "no-cache" 
    }
    strRet=""
    time_inter=0
    try:
        time1=0 
        time2=0
        time1=time.time() * 1000
        if strScheme.upper()=="HTTPS": #URLLib中，对于HTTP和HTTPS的连接要求是不同的
            con2 = httplib.HTTPSConnection(strHost)
        else:
            con2 = httplib.HTTPConnection(strHost)
            
        if strMethod.upper()=="POST":
            con2.request(method="POST",url= strURL, body=strParam, headers=headers)
        else:
            con2.request(method="GET",url= strURL, headers=headers)
        r2 = con2.getresponse()
        strRet= r2.read().strip() 
        con2.close
    except BaseException,e:
        print e
        con2.close
    return (time_inter,strRet)

def RunTests(strURL):
    t_url=urlparse.urlparse(strURL)
    strScheme=t_url.scheme
    strHost = t_url.netloc
    strURL1 = t_url.path
    print "Checking " + strURL

                   
    (inter1,html1)=SendHTTPRequest("GET",strScheme,strHost,"","")
    if html1.find("Jet")>=0:
        return True
        print "sucssful"
    else:
        return False
        print "fail"
   
if __name__ == "__main__":
    if len(sys.argv)!=2:
        print "INVALID ARGUMENTS."
        exit()
 
    m_URL=sys.argv[1]
    strartmouth = 8
    endmouth = 9
    for i in range(strartmouth,endmouth):
        for j in range(1,31):
            for k in range(0,23):
                for l in range(0,60):
                    for m in (10,100):
                       RunTests(m_URL + strURL = "/data/backup/2014"+ i + j + k + l + m + "_bak.asp")