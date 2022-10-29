
记录折腾mysql数据库时候遇到的一些问题. 

## Debug

### 反引号的使用

- 用反引号 `` ` `` 包围来避免名字不规范, 例如有写成 `` INSERT INTO `<table_name>` `` 这样的


### 配置目录

- 相关配置说明 [MySQL 配置文件 my.cnf / my.ini 逐行详解](https://kalacloud.com/blog/how-to-edit-mysql-configuration-file-my-cnf-ini)

默认的配置目录

```bash
# mysql 目录
sudo ls /var/lib/mysql
# log
/var/log/mysql/error.log

# 配置文件
sudo vim /etc/mysql/mysql.cnf
```

### mysql 服务重启命令

```bash
# 重启
sudo /etc/init.d/mysql restart
sudo service mysql restart
sudo systemctl restart mysql
```

### 允许远程连接

在默认情况下，MySQL 数据库仅监听本地连接。如果想让外网远程连接到数据库，我们需要修改配置文件，让 MySQL 可以监听远程固定 ip 或者监听所有远程 ip。

在配置文件中 (/etc/mysql/mysql.conf.d/) 中搜索设置;

```yaml
bind-address = 0.0.0.0
```

修改用户远程连接权限

```sql
-- 1) 将用户修改为可远程
RENAME USER 'kalacloud'@'localhost' TO 'kalacloud'@'%';

-- 2)或者新建用户
CREATE USER 'kalacloud-remote'@'%' IDENTIFIED WITH mysql_native_password BY 'password';
-- 表权限
GRANT CREATE, ALTER, DROP, INSERT, UPDATE, DELETE, SELECT, REFERENCES, RELOAD on *.* TO 'kalacloud-remote'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;
```

远程连接

```bash
mysql -P 3306 -u username -h mysql_server_ip -p
```

### 修改、查看字符集

```sql
-- 数据库
ALTER DATABASE test DEFAULT CHARACTER SET utf8mb4;

-- 数据表
ALTER TABLE logtest CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8_general_ci;
-- 仅设置 默认编码
ALTER TABLE logtest DEFAULT CHARACTER SET utf8mb4 COLLATE utf8_general_ci;

-- 某一列
ALTER TABLE logtest CHANGE title title VARCHAR(100) CHARACTER SET utf8 COLLATE utf8_general_ci;
```

查看 database, table, column 的字符集

```sql
SHOW CREATE DATABASE db_name;
SHOW CREATE TABLE tbl_name;
SHOW FULL COLUMNS FROM tbl_name;
```

### 设置变量

- from [stackoverflow](https://stackoverflow.com/questions/11754781/how-to-declare-a-variable-in-mysql)
- [User-defined variables](http://dev.mysql.com/doc/refman/5.0/en/user-variables.html) (prefixed with `@`)

```sql
SET @start = 1, @finish = 10;
-- or
SELECT @start := 1, @finish := 10;

SELECT * FROM places WHERE place BETWEEN @start AND @finish;
```

### 重制 root 密码

from [here](https://help.aliyun.com/document_detail/42520.html)

```bash
# 1. 配置
vim /etc/my.cnf
# 在 [mysqld] 字段下增加
skip-grant-tables

# 2. 重启
/etc/init.d/mysqld restart

# 3. 登陆数据库
/usr/bin/mysql
USE mysql;
# 注意将 [$Password] 替换成想要的密码
UPDATE user SET authentication_string = password ('[$Password]') WHERE User = 'root';
flush privileges;
quit

# 4. 恢复 配置文件, 重启
vim /etc/my.cnf
/etc/init.d/mysqld restart
```

### 查看配置文件

```bash
mysql --help | grep my.conf
# /etc/my.cnf /etc/mysql/my.cnf /usr/etc/my.cnf ~/.my.cnf 
# 在配置文件只查找 log-error, 错误日志的目录
```

### 修改数据目录 datadir

from [here](https://stackoverflow.com/questions/1795176/how-to-change-mysql-data-directory)

```bash
sudo /etc/init.d/mysql stop

# 1. 移动 /var/lib/mysql 到新目录
sudo cp -R -p /var/lib/mysql /newpath

# 2. 修改配置文件
sudo vim /etc/apparmor.d/usr.sbin.mysqld # or perhaps /etc/mysql/mysql.conf.d/mysqld.cnf
# 修改其中的 datadir 条目, 原本应该是 /var/lib/mysql

# 3. 修改配置 AppArmor
sudo vim /etc/apparmor.d/usr.sbin.mysqld
# 查找替换 /var/lib/mysql
sudo /etc/init.d/apparmor reload

# 4. mysql
sudo /etc/init.d/mysql restart
```

### 查询表结构

from [here](https://segmentfault.com/a/1190000007025543)

```sql
-- 1. 下面三个
desc table;
describe table;
show columns from tbale;
-- 2. 查看建表语句
show create table info;
-- 3. information_schema数据库
use information_schema;
select table_name,table_comment from tables where table_schema='study_test_db' and table_name='info';
```

### 取消 --secure-file-priv

默认开启, 限制了mysql 导出文件只能到指定的目录下.

在配置文件中, 设置为空; 重启.

```yaml
[mysqld]
secure_file_priv =
```

## 安装、重装

- 下载 <https://dev.mysql.com/downloads/mysql/>
- 可视化图形界面MySQL Workbench <https://dev.mysql.com/downloads/workbench/>

### macOS 安装

- 到 <https://dev.mysql.com/downloads/mysql/> 下载，我用了 dmg 版本，安装之后可在系统设置中找到一个 MySQL 的图标

```bash
PATH=$PATH:/usr/local/mysql/bin
alias mysql="mysql -u root -p"
```

```sql
-- 远程连接
mysql -h 10.0.1.99 -u root -p

--退出
exit
```

### Ubuntu 重装 mysql

- 安装过程参见 [How To Install MySQL on Ubuntu 20.04](https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-20-04)

```bash
# 删除 mysql
sudo apt-get autoremove --purge mysql-server
sudo apt-get remove mysql-server
sudo apt-get autoremove mysql-server
sudo apt-get remove mysql-common #(非常重要)
# 清理残留数据
dpkg -l |grep ^rc|awk '{print $2}' |sudo xargs dpkg -P

# 安装 mysql
sudo apt-get install mysql-server

# 初始化一个安全配置
sudo mysql_secure_installation
```

存档刚安装好的目录结构:

```bash
(base) ➜  data2 ls /etc/mysql
conf.d  debian.cnf  debian-start  my.cnf  mysql.cnf  mysql.conf.d

(base) ➜  data2 sudo ls /var/lib/mysql
auto.cnf    ca.pem      client-key.pem   ib_buffer_pool  ib_logfile0  ibtmp1  performance_schema  public_key.pem server-key.pem
ca-key.pem  client-cert.pem  debian-5.7.flag  ibdata1       ib_logfile1  mysql   private_key.pem     server-cert.pem sys
```

### Ubuntu 升级 mysql

- [中文经验](https://blog.iphpo.com/blog/2019/05/ubuntu-mysql-5.7-%E7%84%A1%E7%97%9B%E5%8D%87%E7%B4%9A%E5%88%B0-8.0/)
- <https://dev.mysql.com/doc/refman/8.0/en/upgrade-prerequisites.html>


## 用户、权限管理

- 参见 [here](https://www.jianshu.com/p/ec2c94c4398f)

### 新建用户

```sql
-- 新建
-- 采用 mysql_native_password 的方式登录
CREATE USER 'bocom'@'%' IDENTIFIED WITH mysql_native_password BY 'bocom';
create user 用户名@主机 identified by '密码';
create user 'test'@'%' identified by 'testPassword';

-- 查询
select user,host,authentication_string from mysql.user;
```

### 用户权限

记得最后 `flush privileges;` 刷写权限.

```sql
-- 查看用户权限
show grants for bocom@'%';
-- 赋权
-- grants all privileges on bocom.* to 'bocom'@'%';
grant all on bocom.* to 'bocom'@'%';
grant all privileges on zhangsanDb.* to zhangsan@'%';
```

### 删除用户

```sql
-- 删除
drop user 'hetan'@'%';
```

### 用户密码

```sql
-- for MySQL
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'root';
-- for MariaDB
ALTER USER 'root'@'localhost' IDENTIFIED VIA mysql_native_password USING PASSWORD('root');
```

也可以

```bash
sudo mysqladmin -u root password newpassword
```

### mysql 表

```sql
-- 查询
select user,host,authentication_string from mysql.user;
```

### 采用密码登录 root

- 默认为 `sudo mysql` 登录
- 需要将 plugin 设置为 `mysql_native_password` 才能用 `mysql -uroot -p` 登录

```sql
update mysql.user set authentication_string=PASSWORD('123456'), plugin='mysql_native_password' where user='root';
flush privileges;
```
