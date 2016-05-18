# VulScanner
Vulnerability Scanner

目前支持Mongodb 批量扫描、Redis口令爆破、aspcms的备份文件路径猜解

1、Mongodb扫描

批量扫描mongodb未授权验证的数据库，并列出数据库名字

需要安装的模块有pymongo 

easy_install pymongo

2、redis口令爆破

支持多线程扫描，可以爆破带有auth的redis。

使用方法：

新建或编辑s.txt文件、然后运行python CrackRedis.py。最终的结果会保存在result.txt中

需要安装的模块有redis

easy_install redis

3、aspcms备份文件路径猜解

根据aspcms中的备份文件名规律。生成相应的文件名，对其进行猜解。


4、svn信息泄露扫描

多线程批量扫描SVN信息泄露漏洞。将待扫描的域名/IP列表保存在url.txt文件，然后执行，扫描完成后的结果保存result.txt文件中

5、用友OA注入和命令执行漏洞扫描程序

批量扫描用友OA注入漏洞和命令执行漏洞。多线程。将待扫描的域名/IP（不需要加HTTP）列表保存在yyoa.txt文件，然后执行，扫描完成后的结果保存yyoaresult.txt文件中

6、docker 未授权扫描漏洞

最新出的docker未授权漏洞批量扫描脚本。多线程。需要把目标保存在ips.txt（不加端口，不加http）。结果保存在result.txt中。


欢迎反馈bug

我的邮箱是Glacier@insight-labs.org

