---
layout: post
title: '运维笔记-概述, Linux命令'
description: 运维
tag: 博客
---     
### 运维概述
    1. 什么是运维
      服务器的运行维护
    2. 名词
      1. IDC(互联网数据中心)
        服务器租用, 机柜租用
      2. 监控软件
        zabbix, nagios, cactti
      3. 常用的Linux操作系统
        1. CentOS
        2. RedHat
        3. Ubuntu
      4. 虚拟化
      5. Web正向代理(客户端知道自己使用的代理IP)
        1. 用途
          1. 访问原来无法访问的资源(google)
          2. 对Web服务器隐藏用户信息
      6. nginx反向代理(客户端没有感觉)
        1. 流程
          客户端 -> 反向代理服务器 -> 把请求转发给内部网络的服务器
        2. 作用
          1. 保证内网安全, 可以使用反向代理提供WAF功能, 阻止WEB攻击
          2. 负载均衡, 优化网站的负载
      7. 负载均衡规则
        1. 轮询: 逐一循环调度
        2. 权重(weight): 指定轮询几率, 权重值和访问比例成正比
        3. ip_hash: 根据客户端IP分配固定的后端服务器
      8. 负载均衡实现(修改nginx配置文件)
        upstream server{#定义集群
            server 10.10.10.11;
            server 10.10.10.12 weight=2;
            server 10.10.10.13;
            server 10.10.10.14 backup;
        }
        server{
            listen 80;
            ... ...
        }

### Linux常用命令
    1. ifconfig: 查看IP地址和MAC地址
      ## Windows中为ipconfig
    2. ping: 测试网络连通性
      ping IP地址/域名 -c 2
    3. nslookup: 解析域名对应的IP地址
      nslookup 域名
    4. top: Linux下的任务管理器, 能够动态显示当前所有进程CPU以及内存的使用率, q退出
    5. ps -aux: 显示系统进程(PID号)
       ps -aux | grep "mysql"
    6. kill: 杀死一个进程
      sudo kill PID号
    7. df -h: 产看磁盘使用情况
    8. ls -lh: l表示长格式, h提供易读单位
      ls -lh 文件名
    9. chmod: 修改文件权限
      chmod +x 文件名
      chmod 644 文件名
          rw-r--r--
      r: 4
      w: 2
      x: 1
    10. wc -1: 统计文件的行数
      wc -l /etc/passwd: 统计Linux系统有多少个用户
    11. sort: 对文件中的内容进行排序
    12. uniq -c
      1. 作用: 去除重复行, 并统计每行出现的次数(相邻行)
      2. 用法: sort 文件名 | uniq -c
    13. find: 根据指定条件查找文件/目录
      1. -name: 文件名查找
         -iname: 不区分大小写
        find 路径 -name "文件名"
        1. 查找 ~/spider目录中的所有 py 文件
          find ~/spider -name "*.py"
      2. -type: 根据类型查找(文件|目录)
        1. 常用选项
          f: 文件
          d: 目录
          l: 链接(link快捷方式)
        2. 查找主目录下以mysql开头的文件
          find ~ -name "mysql*" -type f
        3. -size: 按大小查找
          1. +: 大于...的文件/目录
          2. -: 小于...的文件/目录
          3. 查找/home/tarena/software大于20M的文件
            find ~/software -size +20M -type f
        4. -ctime: 根据时间查找
          1. -ctime +1: 1天以前的文件/目录
          2. -ctime -1: 1天以内的文件/目录
          3. -cmin -5: 5分钟以内的文件/目录
          4. 查找~/spider下1天以内的文件
            find ~/spider -ctime -1 -type f
        5. 处理动作
          find ... -exec Linux命令 {} \;
          1. 查找1天以内的以.doc结尾的文件, 然后删除
            find -ctime -1 -name "*.doc" -type f -exec rm -rf {} \;
    14. ssh: 远程连接到服务器
      1. 格式: ssh 用户名 @ip
      2. 示例: ssh tarena @10.8.44.142
    15. scp
      1. 远程复制文件/目录
      2. scp 文件名 用户名@IP地址:绝对路径
        scp aaa.tar.gz tarena@x.x.x.x:/home/tarena
    16. du -sh: 显示当前目录大小
      du -sh 目录名

### 运维工具
    1. xshell(软件, 安装在windows)
      安全终端的模拟软件
    2. xshell使用方法
      文件 - 新建 - 输入服务器IP地址 - 用户名 - 密码 - 确认连接
    3. Windows <--> Linux
      1. 安装lrzsz
        sudo apt-get install lrzsz
      2. Windows文件 -> Linux
        xshell终端:$ rz
      3. Linux文件 -> Windows
        xshell终端:$ sz 文件名

### 周期性计划任务
    1. 进入周期性计划任务
      $ crontab -e
      按 3
    2. 设置周期性计划任务
      * * * * * python3 /home/tarena/backup.py
      分 时 日 月 周
      分: 0-59
      时: 0-23
      日: 1-31
      月: 1-12
      周: 0-6

      *: 代表所有可能性
      ,: 指定多个时间点
        每个月的1日和5日的00:00执行1个py文件
        0 0 1,5 * * python3 /home/tarena/backup.py
      /: 指定时间间隔的频率
        每隔10分钟执行1个py文件
        */10 * * * * python3 /home/tarena/backup.py
      -: 指定一个时间段
        0点-6点之间, 每小时执行1个py文件
        0 0-6/1 * * * python3 /home/tarena/backup.py
      练习
        1. 每分钟执行1次backup.py
          */1 * * * * python3 /home/tarena/backup.py
        2. 每小时的第3分钟和第15分钟执行backup.py
          3,15 * * * * python3 /home/tarena/backup.py
        3. 每周六和周日的0点执行backup.py
          0 0 * * 6,0 python3 /home/tarena/backup.py
        4. 每天的18点-23点之间, 每小时执行1次backup.py
          0 18-23/1 * * * python3 /home/tarena/backup.py

### awk的使用
    1. 语法格式: awk 选项 "动作" 文件
    2. 用法: Linux命令 | awk 选项 '动作'
    3. 使用示例
      1. awk '{print "hello"}' ip.txt
      2. df -h | awk '{print $1}'
        作用: 显示df -h结果第一列的内容(默认以空白分隔不同的列)
      3. awk -f "分隔符" '{动作}' ...
        ## 默认以空白分隔, -F可手动指定分隔符
      4. 显示本机的IP地址
        ifconfig | head -2 | tail -1 | awk '{print $2}' | awk -F ":" '{print $2}'
      5. nginx的访问日志目录: /var/log/nginx/access.log
        1. 把访问过自己的IP地址输出
        2. 统计一共有多少个IP访问地址
        3. 输出访问我最多的 IP 和 访问次数
        4. sort的参数
          sort -k 1: 按照第1列进行排序
          sort -n: 以数字的方式比较排序
          sort -r: 倒序排序
          sort -rnk 1: 把第1列以数字的方式进行倒序排列

### shell编程
    1. 解释执行器
      1. sh
      2. bash
        ## /etc/passwd查看用户默认bash, sh解释执行器没有高亮显示, 也没有自动补全
    2. shell编程
      1. 所有的shell程序都是以 .sh 结尾
      2. 执行方式
        1. bash
        2. chmod +x test.sh
          ./test.sh
          ## 保证文件中第一行行为: #!/bin/bash
    3. shell基础
      1. 变量赋值
        1. 变量名=值: = 两侧不能有空格
          number=10 name="张三丰"
        2. 获取Linux命令的执行结果给变量赋值
          1. time=$(date)
          2. time='date'
        3. 接收用户从终端输入给变量赋值
          read -p "提示信息" 变量名
          read -p "输入姓名" 变量名
      2. 输出语句
        echo $变量名
      3. '' 和 "" 的区别
        1. '' 无法获取变量的值
        2. "" 可以获取变量的值
          read -p "Input Name:" name # 张三丰
          echo '名字是:$name' 结果: 名字是:$name
          echo "名字是:$name" 结果: 名字是:张三丰
      4. 运算符
        1. 算术运算符
          + - * / %
          ++: 自加1运算
          --
          运算命令(let):
            1. let运算表达式
              i=1
              let i++
              echo $i
            2. expr运算表达式
              i=1
              sum = `expr $1 + 5`
              echo $sum
        2. 比较运算符
          1. 文件状态
            -e: 文件/目录是否存在
            -d: 判断是否为目录
            -f: 判断是否为文件
          2. 字符比较
            = !=
            空: -z
            非空: !-z 或 -n
          3. 数值比较
            等于: -eq
            大于: -gt
            大于等于: -ge
            小于: -lt
            小于等于: -le
            不等于: -ne
          4. 逻辑比较
            逻辑与: &&
            逻辑或: ||
      5. if条件判断
        1. 语法格式
          if [ 条件 ];then
              执行语句
          elif [ ];then
              执行语句
          else
              执行语句
          fi
      6. for循环1
        1. 语法格式
          for 变量名 in 值列表
          do
              执行语句
          done
        2. 造数方法: seq 起始值 步长 终止值
          seq 5: 1 2 3 4 5
          seq 1 2 10: 1 3 5 7 9
          seq 2 2 10: 2 4 6 8 10
        3. 用for循环输出1 2 3 4 5
      7. C-for循环
        1. 语法格式
          for((赋初值;条件判断;步长))
          do
              执行语句
          done
        2. C-for循环输出1 2 3 4 5
      8. while循环
        1. 语法格式
          while [ 条件 ]
          do
              执行语句
          done
        2. 输出1-10之间的整数
      9. 函数
        1. 语法格式
          函数名(){
              代码块
          }
          # 函数调用
          函数名
        2. 在用户主目录创建一个文件夹, 如果不存在就创建, 如果存在就提示用户已存在
    4. 每个五分钟检查根分区使用量, 低于20G时发出警告  
      #!/bin/bash
      while [ 1 -eq 1 ]
      do
          h=`df -h | grep "/$" | awk '{print $4}' | awk -F "G" '{print $1}'`
          if [ $h -lt 20 ];then
              echo "根分区将满,请输出不必要的文件"
          fi  
          sleep 300
      done
    5. 数据库备份
      #!/bin/bash
      day=$(date +%F)
      dir=/home/tarena/mydir
      mysqldump -hlocalhost -uroot -p123456 webdb > $dir/webdb-$(date +%F).sql &> /dev/null
      echo "数据库备份成功"

      计划任务操作
      crontab -e
      0 18 * * * bash /home/tarena/sh/backup.sh
