# MySQL Note

!!! note
    廖雪峰教程笔记 + 实践记录

内容比较杂乱

- 用户、权限管理
- MySQL 基础命令: 常用命令记录
- 基本概念 以下: 教程摘录

参考

- 廖雪峰 [SQL 教程](https://www.liaoxuefeng.com/wiki/1177760294764384)；

基本指令

- DDL(create,drop,alter,truncate)
- DML(update,delete,insert)
- DQL(select)

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
-- 还可以通过这种方式进行「移动」到不同数据库
ALTER TABLE db1.student RENAME db2.student
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


### 查看数据库/表大小: information_schema

```sql
SELECT 
    TABLE_SCHEMA AS `Database`,
    TABLE_NAME AS `Table`,
    ROUND(((DATA_LENGTH + INDEX_LENGTH) / 1024 / 1024), 2) AS `Size (MB)`
FROM information_schema.TABLES
-- 选择单张表
-- WHERE table_schema = "<database name>" 
ORDER BY (DATA_LENGTH + INDEX_LENGTH) DESC;
```

或者

```sql
USE information_schema;

-- 查询库的大小
SELECT TABLE_SCHEMA, SUM(DATA_LENGTH) FROM TABLES GROUP BY TABLE_SCHEMA;
-- 以 k 为单位
SELECT TABLE_SCHEMA, SUM(DATA_LENGTH)/1024 FROM TABLES GROUP BY TABLE_SCHEMA;

-- 查询每张表
SELECT table_name,table_rows,data_length+index_length, 
CONCAT(ROUND((data_length+index_length)/1024/1024,2),'MB')
 DATA FROM information_schema.tables WHERE table_schema='bocom';
```

### 导入导出-mysqldump

#### 数据导出 mysqldump

RUNOOB <https://www.runoob.com/mysql/mysql-database-export.html>

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
