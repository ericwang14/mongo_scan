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

多线程批量扫描SVN信息泄露漏洞。将待扫描的域名/IP列表保存在urlt.txt文件，然后执行，扫描完成后的结果保存result.txt文件中



欢迎反馈bug

我的邮箱是Glacier@insight-labs.org