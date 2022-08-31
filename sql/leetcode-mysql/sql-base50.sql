/* @2208 重温一下mysql
主要 from [50到数据库题](https://blog.csdn.net/qq_44186838/article/details/120499317)
进度: 10/50

todo

- [LeetCode Database习题 && MySQL基础](https://cgiirw.github.io/2018/07/01/MySQL-Getting-Start/)
 */


/* 0175. 组合两个表
给定 Person, Address 两张表, 根据 personId 进行连接. 
注意要求无论 address表中是否有该人, 都要返回该人的信息, 因此对Person进行左连接.
 */
-- 因为题目要求无论 person 是否有地址信息，所以不能用join，要用left join
select FirstName, LastName, City, State 
from Person 
left join Address on Person.PersonId=Address.PersonId


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

/* 0601. 体育馆的人流量 #hard
对于一个记录序列, 要求返回连续的三条记录都是 people>=100 的那些记录. 注意, [F,T,T,T,F] 序列中需要返回中间的全部三条.
思路1: 子连接三次, 然后对于出现在 第1,2,3 位的记录分别考虑 (需要distinct)
思路2: 利用 #窗口函数. 
    最关键的是, 如何分别「连续」的符合条件的记录? 通过 id-rk 来判断, 其中rk是符合条件的记录的 rank.
    这样, 可以保证, 连续的符合条件的记录的 id-rk 的值是一样的. 然后再利用计数进行筛选即可.
 */
select distinct s.*
from Stadium s, Stadium s2, Stadium s3
where (s.people>=100 and s2.people>=100 and s3.people>=100) and (
    -- 注意上面的 and 子句后必须加括号.
    -- 由于我们关心的只有s, 因此不需要考虑 s2,s3 之间的位置关系.
    s.id=s2.id-1 and s.id=s3.id-2 or -- s,s2,s3
    s.id=s2.id+1 and s.id=s3.id-1 or -- s2,s,s3
    s.id=s2.id+2 and s.id=s3.id+1 -- s2,s3,s
)
order by s.id;
-- 思路2: #窗口函数
# 首先是将人流量大于100的数据筛选出来，然后用窗口函数根据id进行排序（一定要是rank而不是dense_rank）
# 利用id-rank，这样就可以将连续的数据分成同一个组（都拥有同一个order1）
# 接着再利用窗口函数根据order1分组并统计各组数量，大于等于3的数据即为所需数据。
SELECT id, visit_date, people
FROM (
    -- 利用窗口函数根据order1分组并统计各组数量，大于等于3的数据即为所需数据。
    SELECT id, visit_date, people, COUNT(*) OVER(PARTITION BY order1) AS order2
    FROM (
        -- 用窗口函数根据id进行排序（一定要是rank而不是dense_rank）
        SELECT *, (id - rank() OVER(ORDER BY id)) AS order1 
        FROM (  
            -- 将人流量大于100的数据筛选出来
            SELECT * FROM Stadium WHERE people >= 100
        ) AS t1
    ) AS t2
) AS t3
WHERE order2 >= 3
order by id;
-- 也可以通过 with 来实现.
-- 采用 #with 关键字
with t1 as(
    select *,id - row_number() over(order by id) as rk
    from stadium
    where people >= 100
)       -- 生成中间表, 其中的将连续的符合条件的的数据的rk设置成一样.
select id,visit_date,people
from t1
where rk in(
    -- 所有符合条件的rk: 出现了三次以上.
    select rk
    from t1
    group by rk
    having count(rk) >= 3
);


/* 1179. 重新格式化部门表 #easy 还是将长表转宽表. 将分散在不同行的按月工资转为宽 
思路1: 通过 group by 进行分组, 然后对于每个列, 可以使用 IF或 CASE 进行判断.
*/
select id,
    SUM(CASE WHEN month="Jan" THEN revenue ELSE NULL END) as "Jan_Revenue",
    SUM(CASE WHEN month="Feb" THEN revenue ELSE NULL END) as "Feb_Revenue",
    SUM(CASE WHEN month="Mar" THEN revenue ELSE NULL END) as "Mar_Revenue",
    SUM(CASE WHEN month="Apr" THEN revenue ELSE NULL END) as "Apr_Revenue",
    SUM(CASE WHEN month="May" THEN revenue ELSE NULL END) as "May_Revenue",
    SUM(CASE WHEN month="Jun" THEN revenue ELSE NULL END) as "Jun_Revenue",
    SUM(CASE WHEN month="Jul" THEN revenue ELSE NULL END) as "Jul_Revenue",
    SUM(CASE WHEN month="Aug" THEN revenue ELSE NULL END) as "Aug_Revenue",
    SUM(CASE WHEN month="Sep" THEN revenue ELSE NULL END) as "Sep_Revenue",
    SUM(CASE WHEN month="Oct" THEN revenue ELSE NULL END) as "Oct_Revenue",
    SUM(CASE WHEN month="Nov" THEN revenue ELSE NULL END) as "Nov_Revenue",
    SUM(CASE WHEN month="Dec" THEN revenue ELSE NULL END) as "Dec_Revenue"
FROM Department
group by id;

/* 0182. 查找重复的电子邮箱 #easy 找到所有重复的邮箱.
思路1: 利用 group by 进行count, 然后筛选 (子查询)
思路1.2: 除了采用临时表, group by 还可以搭配 #HAVING 语法快速筛选.
思路2: 直接 #自连接
 */
select Email
from (
    select Email,count(*) cnt from Person group by Email
) as t1
where cnt>=2;
-- 思路1.2: HAVING 语法快速筛选.
select Email
from Person
group by Email
having count(*)>=2;
-- 思路2: 直接 #自连接
SELECT DISTINCT p1.Email
FROM Person p1, Person p2
WHERE p1.Email=p2.Email AND p1.Id<>p2.Id;

/* 0197. 上升的温度 #easy #题型 要求找到符合条件的日期, 满足当天的温度高于昨天.
思路1: 根据条件进行 #JOIN, 考察 #日期
MySQL 使用 #DATEDIFF 来比较两个日期类型的值。
 */
select w.id
from Weather w 
    join Weather w2 ON DATEDIFF(w.recordDate,w2.recordDate)=1
-- 事实上 where 子句完全可以接到 ON 条件后面. 但速度会更慢?
where w.Temperature>w2.Temperature;


/* 0626. 换座位 #medium #题型
对于id从 1,2,...n, 两两交换座位. 若n为奇数则最后一个不交换.
思路1: 根据座位号进行条件判断: 奇数位+1, 偶数位-1.
思路2: 采用 #位运算 修改学号
    注意到, `(id+1)^1-1` 可以进行奇偶的交换.
    如何处理总数为奇数时的最后一个人? 可以通过 IF来进行判断
思路2.2: 还可以 修改名字! 采用 #COALESCE 函数
    将位运算之后的表与原表进行连接, 采用原来的表的编号. 可理解为「修改名字」
    观察 `seat s1 LEFT JOIN seat s2 ON ((s1.id + 1) ^ 1) - 1 = s2.id`, 对于奇数总数的情况, 最后一条记录为空, 因此用 `COALESCE(s2.student, s1.student)` 进行填充.
 */
SELECT
    (CASE
        WHEN MOD(id, 2) != 0 AND counts != id THEN id + 1
        WHEN MOD(id, 2) != 0 AND counts = id THEN id
        ELSE id - 1
    END) AS id,
    student
FROM
    -- 给 seat 添加一列 counts, 记录所有的座位数量.
    seat, (SELECT COUNT(*) AS counts FROM seat) AS seat_counts
ORDER BY id ASC;
-- 思路2: 采用 #位运算 修改学号
SELECT IF(
    (SELECT COUNT(*) FROM seat)=id AND id%2<>0, id, (id+1)^1-1
) AS id, student
FROM seat
ORDER BY id;
-- 
SELECT
    s1.id, COALESCE(s2.student, s1.student) AS student
FROM
    -- 将位运算之后的表与原表进行连接, 采用原来的表的编号. 可理解为「修改名字」
    -- 对于奇数总数的情况, 最后一个id通过 左连接被去除了. 因此用 #COALESCE 进行补充.
    seat s1
        LEFT JOIN
    seat s2 ON ((s1.id + 1) ^ 1) - 1 = s2.id
ORDER BY s1.id;

/* 620. 有趣的电影 #easy 基本筛选语法 */
select *
from cinema
where description!='boring' and mod(id,2)=1
order by rating desc;

/* 0511. 游戏玩法分析 I #easy
给定一张记录玩家登陆时间的表, 要求查询每个玩家最早的登陆时间
 */
select player_id, min(event_date) first_login from Activity group by player_id;

/* 1097. 游戏玩法分析 V #hard #题型
给定主键为 `(player_id，event_date)` 的游玩记录表. 安装日期定义为玩家第一天登陆游戏的日期. 要求统计「第一天留存率」, 也即在安装日第二天也登陆游戏的玩家比率.
思路1: 对于每一行数据, 利用 #OVER 加上一列安装日期 `first_day`. 然后对于安装日期进行 group by 统计.
    如何计算「第一天留存率」? 对于所有活动记录, 统计 `first_day+1` 有多少人即可.
思路2: 先统计「每个玩家的安装时间」, 然后通过左连接来判断是否在第二天登陆游戏.
 */
# 先取出所有安装日期，然后求出每个安装日期有几个玩家；
# 其中第二天接着玩的有谁(判断玩的日期和安装日期是否相差一天)，就可以了。
SELECT first_day AS install_dt, 
    -- 如何判断当天的装机量? 除了sum之外, 直接用 COUNT(DISTINCT 也可.
    -- sum(event_date=install_dt) AS installs 
    COUNT(DISTINCT player_id) AS installs,
    -- 如何计算「第一天留存率」? 对于所有活动记录, 统计 `first_day+1` 有多少人即可.
    ROUND((SUM(IF(DATEDIFF(event_date, first_day)=1, 1, 0))) / COUNT(DISTINCT player_id), 2) AS Day1_retention
FROM (
    SELECT player_id, event_date, MIN(event_date) OVER(PARTITION BY player_id) AS first_day
    FROM Activity
) AS t1
GROUP BY first_day;
-- 思路2: 先统计「每个玩家的安装时间」, 然后通过左连接来判断是否在第二天登陆游戏.
select a.install_dt,
    count(distinct a.player_id) as 'installs',
    ROUND(count(distinct b.player_id) / count(distinct a.player_id), 2) as `Day1_retention`
from (
    -- 每个玩家的安装日期
    (select player_id, min(event_date) install_dt from Activity group by player_id) AS a
    -- 条件连接, 判断是否在第二天使用了
    left join Activity b
    on a.player_id=b.player_id and DATEDIFF(b.event_date, a.install_dt)=1
) group by install_dt;

/* 0569. 员工薪水中位数 #hard #题型
每个公司有一组薪水记录, 得到每家公司的薪水中位数. 注意如果人数为偶数, 则返回中间的两个数字.
思路1: 利用 #窗口函数 分别统计每个公司中的薪水排名 rk 和公司人数 cnt.
    如何判断是 #中位数? 例如 [1,2,3,4] 中 2,3 是中位数. 
    一种方式是用整除 [(cnt+1)//2, (cnt+2)//2] 可以表示一个/两个中位数. (注意整除可以用 #div 或者 #FLOOR)
    更简单的方法, 不管奇偶性, 中位数一定在 [cnt/2, cnt/2+1] 范围内.
更多思路 [here](https://leetcode.cn/problems/median-employee-salary/solution/si-chong-fang-fa-jie-yuan-gong-xin-shui-gykpa/)
 */
select id,company,salary
from (
    select *,
        row_number() over(partition by company order by salary) rk,
        count(*) over(partition by company) cnt
    from Employee
) as t
-- where rk>=(cnt+1) div 2 and rk<=(cnt+2) div 2;
-- 中位数必定大于一半数同时小于一半数+1
where rk>=cnt/2 and rk<=cnt/2+1;

/* 1841. 联赛信息统计 #medium #题型
有 Matches 表记录了主/客场队得球数. 对于一个赛季的数据, 要求统计每个球队的 比赛次数、得分总数、总进球数、对手球队的所有进球数. 其中分数计算为, 0/1平局/3
排序方式: points 降序, goal_for - goal_against 降序, team_name 字典序.
思路1: 关键点在于 **连接的时候可以用or**, 即 `JOIN ... ON...OR ` 语法
    在本题中, 需要统计球队在 主/客场 的得分情况, 因此需要对于球队添加上参与过的 主/客场 比赛信息.
    即 `Teams t JOIN Matches m ON t.team_id=m.home_team_id OR t.team_id=m.away_team_id`
注意: 这里 Teams 表中 `(team_name, team_id)` 是一一对应的关系. 使用id进行 group, 然后select和order的时候使用name 在逻辑上没错. 但这种方式存在漏洞! 因为数据库无法保障一般情况下也是一一对应的.
    因此, mysql 8.0 默认开启了 `ONLY_FULL_GROUP_BY` 的限制不允许直接使用. 参见 [here](https://kalacloud.com/blog/solve-query-failures-regarding-only-full-group-by-sql-mode/)
    解决方式: 1) 关闭「严格模式」; 2) 采用 #聚合函数 `MAX()`、`MIN()`或者`GROUP_CONCAT()`.
 */
-- 注意, 下面
SELECT team_name,
    COUNT(*) AS 'matches_played', 
    SUM(
        -- 根据不同的情况计算分数
        CASE 
            WHEN (t.team_id=m.home_team_id AND m.home_team_goals>m.away_team_goals) OR
                (t.team_id=m.away_team_id AND m.home_team_goals<m.away_team_goals) THEN 3
            WHEN (t.team_id=m.home_team_id AND m.home_team_goals=m.away_team_goals) OR
                (t.team_id=m.away_team_id AND m.home_team_goals=m.away_team_goals) THEN 1
            WHEN (t.team_id=m.home_team_id AND m.home_team_goals<m.away_team_goals) OR
                (t.team_id=m.away_team_id AND m.home_team_goals>m.away_team_goals) THEN 0
        END
    ) AS 'points', 
    SUM(IF(t.team_id=m.home_team_id, m.home_team_goals, m.away_team_goals)) AS 'goal_for', 
    SUM(IF(t.team_id=m.home_team_id, m.away_team_goals, m.home_team_goals)) AS 'goal_against', 
    -- 统计球队的 进球数-输球数. 这样写好繁琐? 
    SUM(IF(t.team_id=m.home_team_id, m.home_team_goals, m.away_team_goals))-SUM(IF(t.team_id=m.home_team_id, m.away_team_goals, m.home_team_goals)) AS 'goal_diff'
-- 关键点在于 **连接的时候可以用or**
FROM Teams t JOIN Matches m ON t.team_id=m.home_team_id OR t.team_id=m.away_team_id
GROUP BY team_id
ORDER BY points DESC, goal_diff DESC, team_name;
