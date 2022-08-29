/* @2208 重温一下mysql
主要 from [50到数据库题](https://blog.csdn.net/qq_44186838/article/details/120499317)
进度: 10/50
todo

- [LeetCode Database习题 && MySQL基础](https://cgiirw.github.io/2018/07/01/MySQL-Getting-Start/)
 */


/* 0511. 游戏玩法分析 I
给定一张记录玩家登陆时间的表, 要求查询每个玩家最早的登陆时间
 */
select player_id, min(event_date) first_login from Activity group by player_id;

/* 0175. 组合两个表
给定 Person, Address 两张表, 根据 personId 进行连接. 
注意要求无论 address表中是否有该人, 都要返回该人的信息, 因此对Person进行左连接.
 */
-- 因为题目要求无论 person 是否有地址信息，所以不能用join，要用left join
select FirstName, LastName, City, State 
from Person 
left join Address on Person.PersonId=Address.PersonId


/* 0176. 第二高的薪水 #easy #题型
给定一张 Employee 薪资表, 要求得到薪资第二高的工资.
思路1: 先得到最高的薪水, 从其他数据中进行筛选.
思路2: 采用 LIMIT 子句, 来得到第二高的数值
    这里有个问题, 就是limit的结果可能为空, 而答案要求此时应该返回null
    思路2.1: 外面套一层 #子查询
    思路2.2: 使用 #IFNULL 子句


SELECT DISTINCT
    Salary AS SecondHighestSalary
FROM
    Employee
ORDER BY Salary DESC
LIMIT 1 OFFSET 1
 */
select max(salary) SecondHighestSalary
from Employee
where salary < (select max(salary) from Employee); 
-- 思路2.1: 外面套一层 #子查询
SELECT
    (SELECT DISTINCT
            Salary
        FROM
            Employee
        ORDER BY Salary DESC
        LIMIT 1 OFFSET 1) AS SecondHighestSalary
;
-- 路2.2: 使用 #IFNULL 子句
SELECT
    IFNULL(
      (SELECT DISTINCT Salary
       FROM Employee
       ORDER BY Salary DESC
        LIMIT 1 OFFSET 1),
    NULL) AS SecondHighestSalary

/* 0184. 部门工资最高的员工 #medium
有 Employee和Department 根据部门id进行连接. 要求返回每个部门工资最高的员工信息
思路1: 通过 group 语句得到每个部门的最高公司 (作为 #临时表), 然后通过 #join 两张基本表获得相关信息.
*/
SELECT
    Department.name AS 'Department',
    Employee.name AS 'Employee',
    Salary
FROM
    -- join Employee and Department
    Employee
        JOIN
    Department ON Employee.DepartmentId = Department.Id
WHERE
    (Employee.DepartmentId , Salary) IN
    --子查询, 获得每个部门最高工资
    (   SELECT
            DepartmentId, MAX(Salary)
        FROM
            Employee
        GROUP BY DepartmentId
    )
;


/* 0177. 第N高的薪水 #medium #题型
实现一个函数, 要求返回第N高的薪水 (去重).
[here](https://leetcode.cn/problems/nth-highest-salary/solution/mysql-zi-ding-yi-bian-liang-by-luanz/) 介绍了六种方法, 解释了 「MySQL通用查询策略」
思路1: 单表查询 对于salary去重然后排序.
    如何 #去重? 一种方式是使用 #DISTINCT 子句, 另一种方式是使用 #GROUP BY 子句.
    如何得到第N大的数字? 使用 #LIMIT 子句. 注意到, 先要取 M=N-1, 然后用 `LIMIT M 1` 或 `LIMIT 1 OFFSET M` 得到.
    注：这里不能直接用limit N-1是因为limit和offset字段后面只接受正整数（意味着0、负数、小数都不行）或者单一变量（意味着不能用表达式），也就是说想取一条，limit 2-1、limit 1.1这类的写法都是报错的。
思路2: #子查询
    对于每一条记录的salary, 通过子查询 `(SELECT count(DISTINCT salary) FROM employee WHERE salary>e.salary) = N-1` 判断是否是第N大的数字.
    注意这样会有多条的相同记录, 结果需要去重 `SELECT DISTINCT e.salary FROM employee e`.
思路3: #自连接
    「一般来说，能用子查询解决的问题也能用连接解决。」
思路4: 也容易将思路2, 写成笛卡尔积的形式.
思路5：自定义变量
思路6：利用# 窗口函数
    窗口函数: `row_number, rank, dense_rank, ntile`, 需要配合 `over()`, 该函数的参数一般有 `partition by, order by`.
 */
-- 思路0, 写成规范的函数形式.
CREATE FUNCTION getNthHighestSalary(N INT) RETURNS INT
BEGIN
    # i 定义变量接收返回值
    DECLARE ans INT DEFAULT NULL;  
    # ii 执行查询语句，并赋值给相应变量
    SELECT 
        DISTINCT salary INTO ans
    FROM 
        (SELECT 
            salary, @r:=IF(@p=salary, @r, @r+1) AS rnk,  @p:= salary 
        FROM  
            employee, (SELECT @r:=0, @p:=NULL)init 
        ORDER BY 
            salary DESC) tmp
    WHERE rnk = N;
    # iii 返回查询结果，注意函数名中是 returns，而函数体中是 return
    RETURN ans;
END

--  思路1: 单表查询 对于salary去重然后排序.
CREATE FUNCTION getNthHighestSalary(N INT) RETURNS INT
BEGIN
    -- 设置 offset
  SET N := N-1;
  RETURN (
    --   # Write your MySQL query statement below.
    --   select IFNULL(
    --       (select distinct salary from Employee 
    --       order by salary DESC
    --       LIMIT 1 OFFSET N), NULL
    --     -- 等价于 LIMIT N, 1 的形式
    --   )
    select salary from Employee
    group by salary     -- group 操作要在order之前
    order by salary DESC
    LIMIT 1 OFFSET N
  );
END
-- 思路2: #子查询
CREATE FUNCTION getNthHighestSalary(N INT) RETURNS INT
BEGIN
  RETURN (
      SELECT 
          DISTINCT e.salary -- 对结果去重
      FROM 
          employee e
      WHERE 
          (SELECT count(DISTINCT salary) FROM employee WHERE salary>e.salary) = N-1
  );
END
-- 思路3: #自连接. 但下面的代码有问题? 不知道为啥
CREATE FUNCTION getNthHighestSalary(N INT) RETURNS INT
BEGIN
  RETURN (
      SELECT 
          e1.salary
      FROM 
          employee e1 JOIN employee e2 ON e1.salary <= e2.salary
      GROUP BY 
          e1.salary
      HAVING 
          count(DISTINCT e2.salary) = N
  );
END
-- 思路4: 写成笛卡尔积的形式.
CREATE FUNCTION getNthHighestSalary(N INT) RETURNS INT
BEGIN
  RETURN (
      SELECT 
          e1.salary
      FROM 
          employee e1, employee e2 
      WHERE 
          e1.salary <= e2.salary
      GROUP BY 
          e1.salary
      HAVING 
          count(DISTINCT e2.salary) = N
  );
END
-- 思路5：自定义变量
CREATE FUNCTION getNthHighestSalary(N INT) RETURNS INT
BEGIN
  RETURN (
      # Write your MySQL query statement below.
      SELECT 
          DISTINCT salary 
      FROM 
          (SELECT 
                salary, @r:=IF(@p=salary, @r, @r+1) AS rnk,  @p:= salary 
            FROM  
                employee, (SELECT @r:=0, @p:=NULL)init 
            ORDER BY 
                salary DESC) tmp
      WHERE rnk = N
  );
END
-- 思路6：窗口函数
CREATE FUNCTION getNthHighestSalary(N INT) RETURNS INT
BEGIN
  RETURN (
    select distinct salary
    from (
        select salary, dense_rank() over(order by salary DESC) AS rnk
        from Employee
    ) tmp
    where rnk = N
  );
END


/* 0180. 连续出现的数字 #medium
对于顺序的一些序列, 对于某一列, 查找至少连续出现过3次的数字.
 */
select distinct l1.num as ConsecutiveNums 
from Logs l1, Logs l2, Logs l3
where l1.Id=l2.Id-1 and l2.Id=l3.Id-1 and l1.Num=l2.Num and l2.Num=l3.Num;

/* 0185. 部门工资前三高的所有员工 #hard
对于每一个部门, 得到工资前3高的员工信息.
思路1: 要求前3高, 也即部门中员工的工资比他高的应该 <3, 可以用 #子查询 来验证.
    为了得到部门信息, 需要连接 employee 和 department 表.
思路2: 利用 #窗口函数 dense_rank() 得到每个员工的排名
 */
select d.name as 'Department', e.name as 'Employee', e.salary as Salary
from 
    Employee e join Department d 
    on e.departmentId=d.id
where 3 > (
	select count(distinct e2.salary)
    from Employee e2
    where e2.departmentId = e.departmentId and e2.salary>e.salary
);

-- 窗口函数 dense_rank(),能够对各个部门的工资进行排序
SELECT Department,Employee,Salary
FROM (
    SELECT
        d.Name AS Department,
        e.Name AS Employee,
        e.Salary AS Salary,
        DENSE_RANK() OVER (PARTITION BY e.DepartmentId ORDER BY e.Salary DESC) AS rk 
    FROM
        Employee e
        JOIN Department d
        ON e.DepartmentId = d.Id
) AS t
WHERE rk<=3

/* 1777. 每家商店的产品价格 #easy #题型
产品在不同的商店有不同的价格, 要求从长表 [product, store, price] 转为宽表 [product, store1, store2, store3].
关联: 同题1795. 每个产品在不同商店的价格，正好相反
思路1: #IF 语法
思路2: #CASE 语法
 */
-- 这里的聚合函数用 sum, min 等都行, 其实最多只有一个值.
SELECT 
    product_id, 
    SUM(IF(store='store1', price, NULL)) store1,
    SUM(IF(store='store2', price, NULL)) store2,
    SUM(IF(store='store3', price, NULL)) store3
FROM
    Products
GROUP BY product_id
-- 思路2: #CASE 语法
SELECT 
    product_id, 
    MIN(CASE store WHEN 'store1' THEN price ELSE null END) AS store1, 
    MIN(CASE store WHEN 'store2' THEN price ELSE null END) AS store2, 
    MIN(CASE store WHEN 'store3' THEN price ELSE null END) AS store3
FROM products
GROUP BY product_id

/* 1795. 每个产品在不同商店的价格 #easy #题型
1777 的反操作, 宽表转长表.
 */
SELECT product_id, 'store1' store, store1 price FROM products WHERE store1 IS NOT NULL
UNION
SELECT product_id, 'store2' store, store2 price FROM products WHERE store2 IS NOT NULL
UNION
SELECT product_id, 'store3' store, store3 price FROM products WHERE store3 IS NOT NULL;

/* 0178. 分数排名 #medium
给定一组分数, 要求降序排列, 并且计算rank (重复值的rank相同, 连续rank).
思路1: 要计算rank, 可以通过 #子查询统计在所有人中分数大于等于的数量.
    复杂度: O(n^2)
注意, rank 是关键词, 需要转为字符串.
 */
select
    s.score,
    (select count(distinct s2.score) from Scores s2 where s2.score>=s.score) as `rank`
from Scores s
order by s.score desc;

/* 0181. 超过经理收入的员工 #easy 简单连接查询 */
select e.name Employee
from Employee e left join Employee e2 on e.managerId=e2.id
where e.salary>e2.salary;


/* 0262. 行程和用户 #hard 复杂的条件判断 + 比率计算
有 Trips, Users 前者记录不同时间段的行程, 后者记录不同用户的信息 (包括用户和司机). 要求返回每一天, 非禁止用户 (用户和司机可能被ban) 的「取消率」, 也即当天的 取消订单/所有订单数. 结果四舍五入保留两位小数.
思路1: 首先, 将Trips和users表两次连接, 得到司机和乘客的信息, 并将ban用户过滤掉.
    如何计算「取消率」? 可以使用 `SUM(IF(*, 1,0))` 的形式进行计数.
 */
select 
    t.request_at Day,
    (
        round(
            sum(if(t.status!="completed", 1, 0)) / count(*),
            2
        )
    ) as `Cancellation Rate`
from Trips t 
    join Users u1 on t.client_id=u1.users_id
    join Users u2 on t.driver_id=u2.users_id
    -- JOIN Users u1 ON (t.Client_Id=u1.Users_Id AND u1.Banned='No')
    -- JOIN Users u2 ON (t.Driver_Id=u2.Users_Id AND u2.Banned='No')
where 
    t.request_at between "2013-10-01" and "2013-10-03"
    and u1.banned='No' and u2.banned='No'
group by t.request_at


