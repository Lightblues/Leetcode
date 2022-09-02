# MySQL Note

!!! note
    廖雪峰教程笔记 + 实践记录

内容比较杂乱

- Debug: 实际遇到的一些问题记录
- 安装
- 用户、权限管理
- MySQL 基础命令: 常用命令记录
- 概念深入理解: 记录看过的一些原理性文章
- 基本概念 以下: 教程摘录

参考

- 廖雪峰 [SQL 教程](https://www.liaoxuefeng.com/wiki/1177760294764384)；

基本指令

- DDL(create,drop,alter,truncate)
- DML(update,delete,insert)
- DQL(select)

## 杂项

- 用反引号 `` ` `` 包围来避免名字不规范, 例如有写成 `` INSERT INTO `<table_name>` `` 这样的

## Debug

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

## MySQL 基础命令

#### 数据库操作

在一个运行MySQL的服务器上，实际上可以创建多个数据库（Database）。要列出所有数据库，使用命令

```sql
SHOW DATABASES;
```

其中，`information_schema`、`mysql`、`performance_schema`和`sys`是系统库，不要去改动它们。其他的是用户创建的数据库。

```sql
-- 创建
CREATE DATABASE test;
CREATE DATABASE IF NOT EXISTS 数据库名 DEFAULT CHARSET utf8 COLLATE utf8_general_ci; -- 设定编码集为utf8
-- 删除
DROP DATABASE test;
-- 对一个数据库进行操作时，要首先将其切换为当前数据库
USE test;
```

#### 表操作

```sql
--列出当前数据库的所有表
SHOW TABLES;
--查看表的结构
DESC students;
--查看创建表的 SQL 语句
SHOW CREATE TABLE students;

-- 创建
CREATE TABLE table_name (column_name column_type);
-- 设置: NOT NULL; AUTO_INCREMENT; PRIMARY KEY
-- ENGINE设置存储引擎，CHARSET设置编码；

--删除表
DROP TABLE students;
-- drop整表删除，truncate会保留表结构，delete一般用在有条件删除部分表数据的情况

--修改表
ALTER TABLE students ADD COLUMN birth VARCHAR(10) NOT NULL;
ALTER TABLE students CHANGE COLUMN birth birthday VARCHAR(20) NOT NULL; --修改birth列，例如把列名改为birthday，类型改为VARCHAR(20)
ALTER TABLE students DROP COLUMN birthday;
```

#### 表数据操作

```sql
-- 插入数据
INSERT INTO table_name ( field1, field2,...fieldN )
                       VALUES
                       ( value1, value2,...valueN );

-- 查询数据
SELECT column_name,column_name
FROM table_name
[WHERE Clause]
[LIMIT N][ OFFSET M] -- offset 默认为0. limit N,M ：相当于offset N limit M，从第N条记录开始，返回M条记录

-- 更新
UPDATE table_name SET field1=new-value1, field2=new-value2
[WHERE Clause]

-- 删除
DELETE FROM table_name [WHERE Clause]

-- ====================================
-- WHERE
SELECT field1, field2,…fieldN FROM table_name1, table_name2…
WHERE condition1 [AND [OR]] condition2…

-- LIKE
-- 'a%'     //以a开头的数据
-- '%a%'    //含有a的数据
-- '_a_'    //三位且中间字母是a的

-- UNION (ALL)
-- UNION操作符用于连接两个以上的SELECT语句，将结果组合到一个集合中，多个SELECT语句会删除重复的数据
-- UNION ALL 保留重复的值

-- ORDER BY
ORDER BY field1, [field2...] [ASC [DESC]]
ORDER BY CONVERT([xxxxx] using gbk);

-- GROUP BY
GROUP BY column_name;
```


### 查看数据库大小: information_schema

查询库的大小

```sql
USE information_schema;
SELECT TABLE_SCHEMA, SUM(DATA_LENGTH) FROM TABLES GROUP BY TABLE_SCHEMA;

-- 以 k 为单位
SELECT TABLE_SCHEMA, SUM(DATA_LENGTH)/1024 FROM TABLES GROUP BY TABLE_SCHEMA;
```

另参 RUNOOB <https://www.runoob.com/mysql/mysql-database-export.html>

查询每张表

```sql
SELECT table_name,table_rows,data_length+index_length, 
CONCAT(ROUND((data_length+index_length)/1024/1024,2),'MB')
 DATA FROM information_schema.tables WHERE table_schema='bocom';
```

### 数据导出 mysqldump

```sql
-- 导出数据库用mysqldump命令，-p 然后回车之后输入密码
mysqldump -u用户名 -p 数据库名 > 数据库名.sql
mysqldump -uroot -p abc > abc.sql
-- table
mysqldump -u username -ppassword database_name table_name > single_table_dump.sql
-- query
mysqldump -u username -ppassword database_name table_name --where="date_created='2013-06-25' limit 100" > few_rows_dump.sql
-- 只导出表结构
mysqldump -uroot -p -d abc > abc.sql
```

#### 数据导入: .sql 脚本

两种方法，开始前要在 mysql 建立数据库 `create database abc;`

方法一：在mysql命令行中采用 source

```sql
--（1）选择数据库
use abc;
--（2）设置数据库编码
set names utf8;
--（3）导入数据（注意sql文件的路径）
source /home/abc/abc.sql;
```

方法二：

```sql
mysql -u用户名 -p密码 数据库名 < 数据库名.sql
mysql -uroot -p abc < abc.sql
```

### 实用 SQL 语句

#### 插入或替换

如果我们希望插入一条新记录（INSERT），但如果记录已经存在，就先删除原记录，再插入新记录。此时，可以使用REPLACE语句，这样就不必先查询，再决定是否先删除再插入：

```sql
REPLACE INTO students (id, class_id, name, gender, score) VALUES (1, 1, '小明', 'F', 99);
```

若id=1的记录不存在，REPLACE语句将插入新记录，否则，当前id=1的记录将被删除，然后再插入新记录。

#### 插入或更新

如果我们希望插入一条新记录（INSERT），但如果记录已经存在，就更新该记录，此时，可以使用 `INSERT INTO ... ON DUPLICATE KEY UPDATE ...` 语句：

```sql
INSERT INTO students (id, class_id, name, gender, score) VALUES (1, 1, '小明', 'F', 99) ON DUPLICATE KEY UPDATE name='小明', gender='F', score=99;
```

若id=1的记录不存在，INSERT语句将插入新记录，否则，当前id=1的记录将被更新，更新的字段由UPDATE指定。

#### 插入或忽略

如果我们希望插入一条新记录（INSERT），但如果记录已经存在，就啥事也不干直接忽略，此时，可以使用 `INSERT IGNORE INTO ...` 语句：

```sql
INSERT IGNORE INTO students (id, class_id, name, gender, score) VALUES (1, 1, '小明', 'F', 99);
```

若id=1的记录不存在，INSERT语句将插入新记录，否则，不执行任何操作。

#### 快照

如果想要对一个表进行快照，即复制一份当前表的数据到一个新表，可以结合CREATE TABLE 和 SELECT：

```sql
-- 对class_id=1的记录进行快照，并存储为新表students_of_class1:
CREATE TABLE students_of_class1 SELECT * FROM students WHERE class_id=1;
```

新创建的表结构和SELECT使用的表结构完全一致。

#### 写入查询结果集

如果查询结果集需要写入到表中，可以结合 INSERT 和 SELECT，将 SELECT 语句的结果集直接插入到指定表中。

例如，创建一个统计成绩的表statistics，记录各班的平均成绩：

```sql
CREATE TABLE statistics (
    id BIGINT NOT NULL AUTO_INCREMENT,
    class_id BIGINT NOT NULL,
    average DOUBLE NOT NULL,
    PRIMARY KEY (id)
);
```

然后，我们就可以用一条语句写入各班的平均成绩：

```sql
INSERT INTO statistics (class_id, average) SELECT class_id, AVG(score) FROM students GROUP BY class_id;
```

确保INSERT语句的列和SELECT语句的列能一一对应，就可以在statistics表中直接保存查询的结果：

#### 强制使用指定索引

在查询的时候，数据库系统会自动分析查询语句，并选择一个最合适的索引。但是很多时候，数据库系统的查询优化器并不一定总是能使用最优索引。如果我们知道如何选择索引，可以使用FORCE INDEX强制查询使用指定的索引。例如：

```sql
SELECT * FROM students FORCE INDEX (idx_class_id) WHERE class_id = 1 ORDER BY id DESC;
```

指定索引的前提是索引`idx_class_id`必须存在。【注意 idx_class_id 的括号是必须的。】

## 概念深入理解

### InnoDB与mySQL 介绍

- [『浅入浅出』MySQL 和 InnoDB](https://draveness.me/mysql-innodb/) | 1708

数据库和实例: 在 Unix 上，启动一个 MySQL 实例往往会产生两个进程，`mysqld` 就是真正的数据库服务守护进程，而 `mysqld_safe` 是一个用于检查和设置 `mysqld` 启动的控制程序，它负责监控 MySQL 进程的执行，当 `mysqld` 发生错误时，`mysqld_safe` 会对其状态进行检查并在合适的条件下重启。

mySQL 架构: 最上面的连接层; 中间的解析、优化、缓存等; 底部真正负责数据的存储和提取的存储引擎 (例如这里的 InnoDB).

在 InnoDB 存储引擎中，所有的数据都被逻辑地存放在表空间中，表空间（tablespace）是存储引擎中最高的存储逻辑单位，在表空间的下面又包括段（segment）、区（extent）、页（page）

#### 数据存储: tablespace, .frm/.idb, ibdata1

MySQL 使用 InnoDB 存储表时，会将**表的定义**和**数据索引**等信息分开存储，其中前者存储在 `.frm` 文件中，后者存储在 `.ibd` 文件中

- InnoDB 中用于存储数据的文件总共有两个部分
    - 一是系统表空间文件，包括 ibdata1、ibdata2 等文件，其中存储了 InnoDB 系统信息和用户数据库表数据和索引，是所有表公用的。
    - 当打开 `innodb_file_per_table` 选项时，`.ibd` 文件就是每一个表独有的表空间，文件存储了当前表的数据和相关的索引数据。

如何存储记录

- 与现有的大多数存储引擎一样，InnoDB 使用 **页** 作为磁盘管理的最小单位；数据在 InnoDB 存储引擎中都是按行存储的，每个 16KB 大小的页中可以存放 2-200 行的记录。
- 页是 InnoDB 存储引擎管理数据的最小磁盘单位，而 B-Tree 节点就是实际存放表中数据的页面

#### 索引: B+Tree

nnoDB 存储引擎在绝大多数情况下使用 B+ 树建立索引，这是关系型数据库中查找最为常用和有效的索引，但是 B+ 树索引并不能找到一个给定键对应的具体值，它只能找到数据行对应的页，然后正如上一节所提到的，数据库把整个页读入到内存中，并在内存中查找具体的数据行。

- 数据库中的 B+ 树索引可以分为聚集索引（clustered index）和辅助索引（secondary index），它们之间的最大区别就是，聚集索引中存放着一条行记录的全部信息，而辅助索引中只包含索引列和一个用于查找对应行记录的『书签』。
    - 聚集索引理解为 PRIMARY KEY

#### 锁

InnoDB 实现了标准的行级锁，也就是共享锁（Shared Lock）和互斥锁（Exclusive Lock）；共享锁和互斥锁的作用其实非常好理解：

- **共享锁（读锁）**：允许事务对一条行数据进行读取；
- **互斥锁（写锁）**：允许事务对一条行数据进行删除或更新；

#### 事务与隔离级别

- ACID 四大特性：原子性（Atomicity）、一致性（Consistency）、隔离性（Isolation）和持久性（Durability）

事务的隔离性是数据库处理数据的几大基础之一，而隔离级别其实就是提供给用户用于在性能和可靠性做出选择和权衡的配置项。

- `RAED UNCOMMITED`：使用查询语句不会加锁，可能会读到未提交的行（Dirty Read）；
- `READ COMMITED`：只对记录加记录锁，而不会在记录之间加间隙锁，所以允许新的记录插入到被锁定记录的附近，所以再多次使用查询语句时，可能得到不同的结果（Non-Repeatable Read）；
- `REPEATABLE READ`：多次读取同一范围的数据会返回第一次查询的快照，不会返回不同的数据行，但是可能发生幻读（Phantom Read）；
- `SERIALIZABLE`：InnoDB 隐式地将全部的查询语句加上共享锁，解决了幻读的问题；

MySQL 中默认的事务隔离级别就是 `REPEATABLE READ`，但是它通过 Next-Key 锁也能够在某种程度上解决幻读的问题。

## 基本概念

### 主键

作为主键最好是完全业务无关的字段，我们一般把这个字段命名为id。常见的可作为id字段的类型有：

- 自增整数类型：数据库会在插入数据时自动为每一条记录分配一个自增整数，这样我们就完全不用担心主键重复，也不用自己预先生成主键；
- 全局唯一GUID类型：使用一种全局唯一的字符串作为主键，类似8f55d96b-8acc-4636-8cb8-76bf8abc2f57。GUID算法通过网卡MAC地址、时间戳和随机数保证任意计算机在任意时间生成的字符串都是不同的，大部分编程语言都内置了GUID算法，可以自己预算出主键。

对于大部分应用来说，通常自增类型的主键就能满足需求。我们在students表中定义的主键也是`BIGINT NOT NULL AUTO_INCREMENT`类型。
【主键是关系表中记录的唯一标识。主键的选取非常重要：主键不要带有业务含义，而应该使用BIGINT自增或者GUID类型。主键也不应该允许NULL。
可以使用多个列作为联合主键，但联合主键并不常用。】

### 外键

外键并不是通过列名实现的，而是通过定义外键约束实现的：

```sql
ALTER TABLE students
ADD CONSTRAINT fk_class_id
FOREIGN KEY (class_id)
REFERENCES classes (id);
```

其中，外键约束的名称 `fk_class_id` 可以任意，`FOREIGN KEY (class_id)` 指定了class_id作为外键，`REFERENCES classes (id)` 指定了这个外键将关联到classes表的id列（即classes表的主键）。
通过定义外键约束，关系数据库可以保证无法插入无效的数据。即如果classes表不存在id=99的记录，students表就无法插入class_id=99的记录。
由于外键约束会降低数据库的性能，大部分互联网应用程序为了追求速度，**并不设置外键约束，而是仅靠应用程序自身来保证逻辑的正确性**。这种情况下，class_id仅仅是一个普通的列，只是它起到了外键的作用而已。

要删除一个外键约束，也是通过ALTER TABLE实现的：

```sql
ALTER TABLE students
DROP FOREIGN KEY fk_class_id;
```

【关系数据库通过外键可以实现一对多、多对多和一对一的关系。外键既可以通过数据库来约束，也可以不设置约束，仅依靠应用程序的逻辑来保证。】

### 索引

如果要经常根据score列进行查询，就可以对score列创建索引：

```sql
ALTER TABLE students
ADD INDEX idx_score (score);
```

使用`ADD INDEX idx_score (score)`就创建了一个名称为idx_score，使用列score的索引。索引名称是任意的，索引如果有多列，可以在括号里依次写上，例如：

```sql
ALTER TABLE students
ADD INDEX idx_name_score (name, score);
```

索引的效率取决于索引列的值是否散列，即该列的值如果越互不相同，那么索引效率越高。反过来，如果记录的列存在大量相同的值，例如gender列，大约一半的记录值是M，另一半是F，因此，对该列创建索引就没有意义。

可以对一张表创建多个索引。索引的优点是提高了查询效率，缺点是在插入、更新和删除记录时，需要同时修改索引，因此，索引越多，插入、更新和删除记录的速度就越慢。

对于主键，关系数据库会自动对其创建主键索引。使用主键索引的效率是最高的，因为主键会保证绝对唯一。

#### 唯一索引

在设计关系数据表的时候，看上去唯一的列，例如身份证号、邮箱地址等，因为他们具有业务含义，因此不宜作为主键。
但是，这些列根据业务要求，又具有唯一性约束：即不能出现两条记录存储了同一个身份证号。这个时候，就可以给该列添加一个唯一索引。例如，我们假设students表的name不能重复：

```sql
ALTER TABLE students
ADD UNIQUE INDEX uni_name (name);
```

通过UNIQUE关键字我们就添加了一个唯一索引。

也可以只对某一列添加一个唯一约束而不创建唯一索引：

```sql
ALTER TABLE students
ADD CONSTRAINT uni_name UNIQUE (name);
```

这种情况下，name列没有索引，但仍然具有唯一性保证。

无论是否创建索引，对于用户和应用程序来说，使用关系数据库不会有任何区别。这里的意思是说，当我们在数据库中查询时，如果有相应的索引可用，数据库系统就会自动使用索引来提高查询效率，如果没有索引，查询也能正常执行，只是速度会变慢。因此，索引可以在使用数据库的过程中逐步优化。

## 查询数据

### 初始化数据库

大佬给的一个 test 数据库：

```sql
-- 如果test数据库不存在，就创建test数据库：
CREATE DATABASE IF NOT EXISTS test;

-- 切换到test数据库
USE test;

-- 删除classes表和students表（如果存在）：
DROP TABLE IF EXISTS classes;
DROP TABLE IF EXISTS students;

-- 创建classes表：
CREATE TABLE classes (
    id BIGINT NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 创建students表：
CREATE TABLE students (
    id BIGINT NOT NULL AUTO_INCREMENT,
    class_id BIGINT NOT NULL,
    name VARCHAR(100) NOT NULL,
    gender VARCHAR(1) NOT NULL,
    score INT NOT NULL,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 插入classes记录：
INSERT INTO classes(id, name) VALUES (1, '一班');
INSERT INTO classes(id, name) VALUES (2, '二班');
INSERT INTO classes(id, name) VALUES (3, '三班');
INSERT INTO classes(id, name) VALUES (4, '四班');

-- 插入students记录：
INSERT INTO students (id, class_id, name, gender, score) VALUES (1, 1, '小明', 'M', 90);
INSERT INTO students (id, class_id, name, gender, score) VALUES (2, 1, '小红', 'F', 95);
INSERT INTO students (id, class_id, name, gender, score) VALUES (3, 1, '小军', 'M', 88);
INSERT INTO students (id, class_id, name, gender, score) VALUES (4, 1, '小米', 'F', 73);
INSERT INTO students (id, class_id, name, gender, score) VALUES (5, 2, '小白', 'F', 81);
INSERT INTO students (id, class_id, name, gender, score) VALUES (6, 2, '小兵', 'M', 55);
INSERT INTO students (id, class_id, name, gender, score) VALUES (7, 2, '小林', 'M', 85);
INSERT INTO students (id, class_id, name, gender, score) VALUES (8, 3, '小新', 'F', 91);
INSERT INTO students (id, class_id, name, gender, score) VALUES (9, 3, '小王', 'M', 89);
INSERT INTO students (id, class_id, name, gender, score) VALUES (10, 3, '小丽', 'F', 85);

-- OK:
SELECT 'ok' AS 'result:';
```

保存为一个 `.sql` 文件，然后执行下面的语句即可~

```bash
mysql -u root -p < init-test-data.sql
```

### 基本查询

```sql
SELECT * FROM <表名>
```

虽然SELECT可以用作计算，但它并不是SQL的强项。但是，不带FROM子句的SELECT语句有一个有用的用途，就是用来判断当前到数据库的连接是否有效。许多检测工具会执行一条 `SELECT 1;` 来测试数据库连接。

### 条件查询

```sql
SELECT * FROM <表名> WHERE <条件表达式>
-- AND OR 语句
SELECT * FROM students WHERE score >= 80 AND gender = 'M';
-- NOT 语句
-- NOT class_id = 2其实等价于class_id <> 2
SELECT * FROM students WHERE NOT class_id = 2;
```

LIKE 语句

`name LIKE 'ab%'` %表示任意字符，例如'ab%'将匹配'ab'，'abc'，'abcd'

查询分数在60分(含)～90分(含)之间的学生可以使用的WHERE语句是：`WHERE score >= 60 AND score <= 90` 或 `WHERE score BETWEEN 60 AND 90`，注意不能用连续的比较符号 WHERE 60 <= score <= 90 或者是 WHERE score IN (60, 90)。

### 投影查询

```sql
SELECT id, score points, name FROM students WHERE gender = 'M';
```

注意上面用了别名

### 排序

```sql
SELECT id, name, gender, score FROM students ORDER BY score DESC;
-- 设定第二个排序准则为 gender
SELECT id, name, gender, score FROM students ORDER BY score DESC, gender;
```

默认的排序规则是ASC：“升序”，即从小到大。ASC可以省略，即ORDER BY score ASC和ORDER BY score效果一样。
如果有WHERE子句，那么ORDER BY子句要放到WHERE子句后面。

### 分页查询

```sql
SELECT id, name, gender, score
FROM students
ORDER BY score DESC
LIMIT 3 OFFSET 0;
```

OFFSET超过了查询的最大数量并不会报错，而是得到一个空的结果集。

OFFSET是可选的，如果只写LIMIT 15，那么相当于LIMIT 15 OFFSET 0。
在MySQL中，`LIMIT 15 OFFSET 30` 还可以简写成 `LIMIT 30, 15`。
使用LIMIT <M> OFFSET <N>分页时，**随着N越来越大，查询效率也会越来越低**。

### 聚合查询

包括 COUNT SUM AVG MAX MIN 等。

```sql
SELECT COUNT(*) num FROM students;
-- AVG
SELECT AVG(score) average FROM students WHERE gender = 'M';
```

要特别注意：如果聚合查询的WHERE条件没有匹配到任何行，COUNT()会返回0，而SUM()、AVG()、MAX()和MIN()会返回NULL。

【例题】每页3条记录，如何通过聚合查询获得总页数？
注意向上取整：`SELECT CEILING(COUNT(*) / 3) FROM students;`

#### 分组

```sql
SELECT class_id, COUNT(*) num FROM students GROUP BY class_id;
-- 多列分组
SELECT class_id, gender, COUNT(*) num FROM students GROUP BY class_id, gender;
```

### 多表查询

【笛卡尔积】

```sql
SELECT
    s.id sid,
    s.name,
    s.gender,
    s.score,
    c.id cid,
    c.name cname
FROM students s, classes c;
```

这种一次查询两个表的数据，查询的结果也是一个二维表，它是students表和classes表的“乘积”，即students表的每一行与classes表的每一行都两两拼在一起返回。结果集的列数是students表和classes表的列数之和，行数是students表和classes表的行数之积。

### 连接查询

```sql
SELECT s.id, s.name, s.class_id, c.name class_name, s.gender, s.score
FROM students s
INNER JOIN classes c
ON s.class_id = c.id;
```

有RIGHT OUTER JOIN，就有LEFT OUTER JOIN，以及FULL OUTER JOIN。它们的区别是：

INNER JOIN只返回同时存在于两张表的行数据，由于students表的class_id包含1，2，3，classes表的id包含1，2，3，4，所以，INNER JOIN根据条件s.class_id = c.id返回的结果集仅包含1，2，3。
RIGHT OUTER JOIN返回右表都存在的行。如果某一行仅在右表存在，那么结果集就会以NULL填充剩下的字段。
LEFT OUTER JOIN则返回左表都存在的行。
最后，我们使用FULL OUTER JOIN，它会把两张表的所有记录全部选择出来，并且，自动把对方不存在的列填充为NULL.

## 修改数据

### INSERT

```sql
INSERT INTO <表名> (字段1, 字段2, ...) VALUES (值1, 值2, ...);

-- 添加多条
INSERT INTO students (class_id, name, gender, score) VALUES
  (1, '大宝', 'M', 87),
  (2, '二宝', 'M', 81);

SELECT * FROM students;
```

### UPDATE

```sql
UPDATE <表名> SET 字段1=值1, 字段2=值2, ... WHERE ...;

-- 更新score<80的记录
UPDATE students SET score=score+10 WHERE score<80;


```

如果WHERE条件没有匹配到任何记录，UPDATE语句不会报错，也不会有任何记录被更新。
【在使用MySQL这类真正的关系数据库时，UPDATE语句会返回更新的行数以及WHERE条件匹配的行数。】

### DELETE

```sql
DELETE FROM <表名> WHERE ...;

DELETE FROM students WHERE id>=5 AND id<=7;
```

## 事务

这种把多条语句作为一个整体进行操作的功能，被称为数据库事务。数据库事务可以确保该事务范围内的所有操作都可以全部成功或者全部失败。如果事务失败，那么效果就和没有执行这些SQL一样，不会对数据库数据有任何改动。

可见，数据库事务具有ACID这4个特性：

- A：Atomic，原子性，将所有SQL作为原子工作单元执行，要么全部执行，要么全部不执行；
- C：Consistent，一致性，事务完成后，所有数据的状态都是一致的，即A账户只要减去了100，B账户则必定加上了100；
- I：Isolation，隔离性，如果有多个事务并发执行，每个事务作出的修改必须与其他事务隔离；
- D：Duration，持久性，即事务完成后，对数据库数据的修改被持久化存储。

对于单条SQL语句，数据库系统自动将其作为一个事务执行，这种事务被称为 **隐式事务**。

要手动把多条SQL语句作为一个事务执行，使用BEGIN开启一个事务，使用COMMIT提交一个事务，这种事务被称为显式事务，例如，把上述的转账操作作为一个显式事务：

```sql
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;

--回滚，主动失败
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
ROLLBACK;
```

相关指令

- `BEGIN` 或 `START TRANSACTION`；显式地开启一个事务；
- `COMMIT` ；也可以使用 `COMMIT WORK`，不过二者是等价的。COMMIT会提交事务，并使已对数据库进行的所有修改成为永久性的；
- `ROLLBACK`；有可以使用 ROLLBACK WORK，不过二者是等价的。回滚会结束用户的事务，并撤销正在进行的所有未提交的修改；
- `SAVEPOINT identifier`；SAVEPOINT允许在事务中创建一个保存点，一个事务中可以有多个SAVEPOINT；
- `RELEASE SAVEPOINT identifier`；删除一个事务的保存点，当没有指定的保存点时，执行该语句会抛出一个异常；
- `ROLLBACK TO identifier`；把事务回滚到标记点；
- `SET TRANSACTION`；用来设置事务的隔离级别。InnoDB存储引擎提供事务的隔离级别有 `READ UNCOMMITTED、READ COMMITTED、REPEATABLE READ、SERIALIZABLE`；

#### 隔离级别

对于两个并发执行的事务，如果涉及到操作同一条记录的时候，可能会发生问题。因为并发操作会带来数据的不一致性，包括脏读、不可重复读、幻读等。数据库系统提供了隔离级别来让我们有针对性地选择事务的隔离级别，避免数据不一致的问题。

| Isolation Level  | 脏读（Dirty Read） | 不可重复读（Non Repeatable Read） | 幻读（Phantom Read） |
|------------------|----------------|----------------------------|------------------|
| Read Uncommitted | Yes            | Yes                        | Yes              |
| Read Committed   | -              | Yes                        | Yes              |
| Repeatable Read  | -              | -                          | Yes              |
| Serializable     | -              | -                          | -                |

### Read Uncommitted

Read Uncommitted是隔离级别最低的一种事务级别。在这种隔离级别下，一个事务会读到另一个事务更新后但未提交的数据，如果另一个事务回滚，那么当前事务读到的数据就是脏数据，这就是**脏读（Dirty Read）**。

```sql
--
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
--
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
--
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
--

```

### Read Committed

在Read Committed隔离级别下，一个事务可能会遇到**不可重复读（Non Repeatable Read）**的问题。
不可重复读是指，在一个事务内，多次读同一数据，在这个事务还没有结束时，如果另一个事务恰好修改了这个数据，那么，在第一个事务中，两次读取的数据就可能不一致。

### Repeatable Read

在Repeatable Read隔离级别下，一个事务可能会遇到**幻读（Phantom Read）**的问题。
幻读是指，在一个事务中，第一次查询某条记录，发现没有，但是，当试图更新这条不存在的记录时，竟然能成功，并且，再次读取同一条记录，它就神奇地出现了。

### Serializable

Serializable是最严格的隔离级别。在Serializable隔离级别下，所有事务按照次序依次执行，因此，脏读、不可重复读、幻读都不会出现。
虽然Serializable隔离级别下的事务具有最高的安全性，但是，由于事务是串行执行，所以效率会大大下降，应用程序的性能会急剧降低。如果没有特别重要的情景，一般都不会使用Serializable隔离级别。

#### 默认隔离级别

如果没有指定隔离级别，数据库就会使用默认的隔离级别。在MySQL中，如果使用InnoDB，默认的隔离级别是Repeatable Read。
