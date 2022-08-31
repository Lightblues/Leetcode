/* 
SQL 学习计划 https://leetcode.cn/study-plan/sql/?progress=gy93tn5

 */
/* ============================================ 第 1 天 选择 ==============================*/
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

/* ============================================ 第 2 天 排序 & 修改 ============================== */

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
-- 因为是删除, 所以不能用下面的 select 语句
-- select min(id),email
-- from Person group by email;
-- 下面的语法不行!!!
-- You can't specify target table 'Person' for update in FROM clause
-- DELETE FROM Person
-- WHERE id NOT IN (
--     SELECT min(id) FROM Person GROUP BY email
-- );
DELETE p
from Person p, Person p2
where p.email=p2.email and p.id>p2.id;

/* ============================================ 第 3 天 字符串处理函数/正则 ==============================
doc: https://dev.mysql.com/doc/refman/8.0/en/string-functions.html
*/
/* 1667. 修复表中的名字 #easy #string
处理字符串, 命名的形式.
相关函数: LEFT(x,len), RIGHT; UPPER(s), LOWER; SUBSTRING(s,5) 得到第5个字符及其之后的子序列.
 */
select user_id, CONCAT(
    UPPER(LEFT(name,1)), LOWER(SUBSTRING(name,2))   -- 等价 RIGHT(name, LENGTH(name)-1)
) name
from Users
order by user_id; 

/* 1484. 按日期分组销售产品 #easy 
按日期得到每天出售的不同产品, 需要对分组的结果进行 #GROUP_CONCAT 操作. (长表转宽表)
 */
select sell_date, count(distinct product) num_sold, GROUP_CONCAT(distinct product) products
from Activities
group by sell_date
order by sell_date;

/* 1527. 患某种疾病的患者 #easy 
患者的一组疾病通过空格进行分割. 筛选出患1型糖尿病的患者 (疾病代码以 DIAB1 开头). 
注意, 代码必须要以DIAB1开头, 并且如果不是第一个的话, 前面会有空格. 
思路1: 根据两个情况写简单的 #正则: `conditions like "DIAB1%" or conditions like "% DIAB1%"`
*/
select *
from Patients
where conditions like "DIAB1%" or conditions like "% DIAB1%";



/* ============================================ 第 4 天 组合查询 & 指定选取 ============================== */
/* 1965. 丢失信息的雇员 #easy 但个人感觉 #medium #题型
名称和工资表分别id, 需要查找仅在一张表中出现过的id.
思路1: 将两张表中 id 都拿出来进行 `UNION ALL`, 然后统计计数为1的那些即可.
    注意 UNION, UNION ALL 的区别: 前者会将重复行进行合并, 后者则是保留.
思路2: 分成「仅在A中出现」和「仅在B中出现」两种情况, 分别写查询, 然后 UNION 即可.
    如何判断id没有在B中出现? 方法很多, 可以用 NOT IN, NOT EXISTS, 也可以通过连表再去判断.
see [here](https://leetcode.cn/problems/employees-with-missing-information/solution/mysql-by-pandaoknight-zpbc/)
 */
--  思路1 UNION ALL
select * from (
    select employee_id from Employees
    UNION ALL
    select employee_id from Salaries
) as tmp
group by employee_id
having count(*)=1
order by employee_id;
-- 思路2: 分成「仅在A中出现」和「仅在B中出现」两种情况, 分别写查询, 然后 UNION 即可.
-- 注意, UNION 的结果是可以直接 ORDER 的, 下面其实不必写临时表.
select * from (
    select employee_id from Employees where employee_id not in (select employee_id from Salaries)
    UNION
    select employee_id from Salaries where employee_id not in (select employee_id from Employees)
) as tmp
order by employee_id;
-- 思路2. 通过连表再去判断.
select e.employee_id employee_id from Employees e left join Salaries s on e.employee_id=s.employee_id where s.employee_id is null
union all
select s.employee_id employee_id from Employees e right join Salaries s on e.employee_id=s.employee_id where e.employee_id is null
order by employee_id;


/* 1795. 每个产品在不同商店的价格 #easy #题型
1777 的反操作, 宽表转长表.
 */
SELECT product_id, 'store1' store, store1 price FROM products WHERE store1 IS NOT NULL
UNION
SELECT product_id, 'store2' store, store2 price FROM products WHERE store2 IS NOT NULL
UNION
SELECT product_id, 'store3' store, store3 price FROM products WHERE store3 IS NOT NULL;


/* 0608. 树节点 #medium #题型
树结构根据 `<id,p_id>` 的形式存储, 要求判断每个节点是 root/inner/leaf.
思路1: 利用 #CASE 进行分类判断 
    如何判断root? 其parent为空. 如何判断Leaf? 写一个子查询, 其不出现在 `p_id` 列中.
    当然, 也可以写成嵌套的 IF 结构.
思路0: 除了比较简洁的条件判断, [官答](https://leetcode.cn/problems/tree-node/solution/shu-jie-dian-by-leetcode/) 中还给了暴力的 UNION 连接的代码.
 */
select t.id, (
    case
    when t.p_id is null then  'Root'
    -- when (select count(*) from Tree t2 where t2.p_id=t.id) = 0 then 'Leaf'
    when t.idd in (select p_id from Tree) then 'Leaf'
    else "Inner" end
) type from Tree t
order by id;
-- 写成嵌套的 IF 结构.
SELECT
    atree.id,
    IF(ISNULL(atree.p_id),
        'Root',
        IF(atree.id IN (SELECT p_id FROM tree), 'Inner','Leaf')) Type
FROM
    tree atree
ORDER BY atree.id

/* 0176. 第二高的薪水 #easy #题型
给定一张 Employee 薪资表, 要求得到薪资第二高的工资.
思路1: 先得到最高的薪水, 从其他数据中进行筛选.
思路2: 采用 LIMIT 子句, 来得到第二高的数值
    select distinct salary from Employees order by salary desc limit 1,1;
    但这里有个问题, 就是limit的结果可能为空, 而答案要求此时应该返回null.
    思路2.1: 外面套一层 #子查询
    思路2.2: 使用 #IFNULL 子句
 */
-- 思路1: 先得到最高的薪水, 从其他数据中进行筛选.
select max(salary) SecondHighestSalary
from Employee
where salary < (select max(salary) from Employee); 
-- 思路2.1: 外面套一层 #SELECT 作为 #临时表
-- 注意这里不是 FROM 语法.
SELECT
    (SELECT DISTINCT Salary
        FROM Employee
        ORDER BY Salary DESC
        LIMIT 1 OFFSET 1) AS SecondHighestSalary;
-- 路2.2: 使用 #IFNULL 子句
SELECT
    IFNULL(
      (SELECT DISTINCT Salary
       FROM Employee
       ORDER BY Salary DESC
        LIMIT 1 OFFSET 1),
    NULL) AS SecondHighestSalary;


/* ============================================ 第 5 天 合并 ============================== */















/* ============================================ 第 6 天 合并 ============================== */

