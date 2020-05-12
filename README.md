#CheckCommDDCW.sh使用说明：
sh CheckCommDDCW.sh  [ any parameters ]

 


#ddcw.spec使用说明
#1.生成rpm包
#rpmbuild -bb ddcw.spec

#CheckCommDDCW.sh使用说明：
sh CheckCommDDCW.sh  [ any parameters ]

 


#ddcw.spec使用说明
#1.生成rpm包
#rpmbuild -bb ddcw.spec

安装：
rpm -ivh ddcw-2020-0428.x86_64.rpm


卸载：
rpm -e ddcw


功能描述：
1.历史记录带时间戳

2.终端PS1显示更好看了

3.扫描端口
#默认扫描本地所有TCP端口 
scanportDDCW
#扫描其它主机端口
scanportDDCW 192.168.112.1
#扫描指定端口
scanportDDCW  22
#扫描指定主机的指定端口
scanportDDCW  127.0.0.1 22
#一直扫描指定主句指定端口，间隔时间1秒
scanportDDCW  127.0.0.1 22  1

4.检查命令是否被修改CheckCommDDCW
sh CheckCommDDCW              #检查命令是否被修改
sh CheckCommDDCW    add   #添加被修改的命令到 ~/.UserCheckCom.txt
https://cloud.tencent.com/developer/article/1597040




使用：
sshNopasswd   [USER@]HOSTNAME[:SSHPORT]  [PASSWORD]


https://cloud.tencent.com/developer/article/1612304




