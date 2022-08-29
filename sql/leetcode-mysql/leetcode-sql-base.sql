/* 
SQL 学习计划 https://leetcode.cn/study-plan/sql/?progress=gy93tn5

 */

/* 0595. 大的国家 #easy
筛选满足两个条件之一的国家 (OR)
 */
select name,population,area from world
where area>=3000000 or population >= 25000000
-- 也可以用 #UNION, 好像会快一点.
select name,population,area from world
where area >= 3000000
UNION
select name,population,area from world
where population >= 25000000;

/* 1757. 可回收且低脂的产品 #easy AND语法 */
select product_id from products
where low_fats='Y' and recyclable='Y';

/* 0584. 寻找用户推荐人 #easy 返回所有某一个key不等于某一值的记录 (可以为空)
注意: 在使用 `!=, <>` 的时候, 记录为NULL的也会删去, 因此要加上一条 `OR [] IS NULL` 判断.
MySQL 使用三值逻辑 —— TRUE, FALSE 和 UNKNOWN。任何与 NULL 值进行的比较都会与第三种值 UNKNOWN 做比较。这个“任何值”包括 NULL 本身！这就是为什么 MySQL 提供 IS NULL 和 IS NOT NULL 两种操作来对 NULL 特殊判断。
 */
select name from customer
where referee_id != 2 or referee_id is null;

/* 0183. 从不订购的客户 #easy 两张表通过id连接, 要求判断在订单表中未出现的用户姓名
利用 #子查询 得到所有订阅过的用户.
 */
select name customers from customers
where customers.id not in (
    select distinct CustomerId from orders
);

/* 1873. 计算特殊奖金 #easy 考察 #条件 语句
思路1: CASE...WHEN...THEN...ELSE...END 语句
思路2: IF(cast,a,b) 语法
相关函数: MOD, LIKE, LEFT(s, n) 取子串
 */
select employee_id, 
(CASE WHEN LEFT(name,1)!='M' and MOD(employee_id,2)!=0 THEN salary
    -- WHEN LEFT(name,1)='M' or MOD(employee_id,2)=0 THEN 0
    ELSE 0 END
) as bonus
from Employees order by employee_id;
-- 
select employee_id, 
    IF(LEFT(name,1)!='M' and MOD(employee_id,2)!=0, salary, 0) as bonus
from Employees order by employee_id

/* 0627. 变更性别 #easy 将性别反转, 考察 update
对于条件判断, 同样可以用 IF或CASE
 */
update Salary
set sex = IF(sex="m", 'f', 'm');
-- 
update Salary
-- 注意下面的括号可以不加, 要加也是 CASE 前.
-- 也可以写成 CASE sex WHEN 'f' THEN 'm' ELSE 'f' END
set sex = (CASE
    WHEN sex='f' THEN 'm'
    ELSE 'f' END
);

/* 0196. 删除重复的电子邮箱 #easy 考察 #DELETE
需要删除重复出现过的邮箱, 保留id最小的.
思路1: 如何检查不是虽小的id? 可以自连接, 检查是否有同名并且id更小的
 */
-- 因为是删除, 所以不能用下面的.
select min(id),email
from Person group by email;
-- 
-- You can't specify target table 'Person' for update in FROM clause
-- DELETE FROM Person
-- WHERE id NOT IN (
--     SELECT min(id) FROM Person GROUP BY email
-- );
DELETE p
from Person p, Person p2
where p.email=p2.email and p.id>p2.id;

