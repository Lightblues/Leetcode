/* 
主要 from [50到数据库题](https://blog.csdn.net/qq_44186838/article/details/120499317)

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

 */
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
-- 思路3: #自连接
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
