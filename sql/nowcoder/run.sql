
-- from https://www.nowcoder.com/exam/oj?page=1&tab=SQL%E7%AF%87&topicId=268

/* SQL156 各个视频的平均完播率
问题：计算2021年里有播放记录的每个视频的完播率(结果保留三位小数)，并按完播率降序排序
思路1: 比例(完播率)的计算
技巧: 时间上的筛选
NOTE: 时间间隔的计算! 要使用 TIMESTAMPDIFF (直接用 - 号可能有问题!)
 */
SELECT
    video_id,
    ROUND(SUM(IF(TIMESTAMPDIFF(SECOND, start_time, end_time) >= duration, 1, 0)) / COUNT(*), 3) AS avg_comp_play_rate
FROM (
    SELECT user.start_time, user.end_time, user.video_id, video.duration
    FROM tb_user_video_log AS user JOIN tb_video_info AS video ON user.video_id = video.video_id
    WHERE user.start_time >= '2021-01-01' AND user.start_time < '2022-01-01'
) AS tmp
GROUP BY video_id
ORDER BY avg_comp_play_rate DESC;
-- from https://www.nowcoder.com/practice/96263162f69a48df9d84a93c71045753?tpId=268&tqId=2285032&ru=/exam/oj&qru=/ta/sql-factory-interview/question-ranking&sourceUrl=%2Fexam%2Foj%3Fpage%3D1%26tab%3DSQL%25E7%25AF%2587%26topicId%3D268
SELECT a.video_id,
        round(sum(if(end_time - start_time >= duration, 1, 0))/count(start_time ),3) as avg_comp_play_rate
FROM 
    tb_user_video_log a LEFT JOIN tb_video_info b on a.video_id = b. video_id
WHERE year(start_time) = 2021       -- 年份筛选
GROUP BY a.video_id 
ORDER BY avg_comp_play_rate DESC;


/* SQL157 平均播放进度大于60%的视频类别
问题：计算各类视频的平均播放进度，将进度大于60%的类别输出。
注：
播放进度=播放时长÷视频时长*100%，当播放时长大于视频时长时，播放进度均记为100%。
结果保留两位小数，并按播放进度倒序排序。
NOTE: 符号上面, 采用 CONCAT 来拼接字符串 */
SELECT tag,
    CONCAT(ROUND(avg_play_rate, 2), '%') AS avg_play_rate
FROM (
    SELECT tag,
        ROUND(AVG(play_rate), 2) AS avg_play_rate
    FROM (
        SELECT tag, 
            -- IF(end_time - start_time > duration, 100, ROUND((end_time - start_time) / duration * 100, 2)) AS play_rate
            IF(TIMESTAMPDIFF(SECOND, start_time, end_time) > duration, 100, TIMESTAMPDIFF(SECOND, start_time, end_time) / duration * 100) AS play_rate
        FROM tb_user_video_log AS user LEFT JOIN tb_video_info AS video ON user.video_id = video.video_id
    ) AS tmp
    GROUP BY tag
    HAVING avg_play_rate > 60
    ORDER BY avg_play_rate DESC
) as tmp;


/* SQL158 每类视频近一个月的转发量/率
问题：统计在有用户互动的最近一个月（按包含当天在内的近30天算，比如10月31日的近30天为10.2~10.31之间的数据）中，每类视频的转发量和转发率（保留3位小数）。
注：转发率＝转发量÷播放量。结果按转发率降序排序。
NOTE: 这里的「最近一个月」, 需要从用户记录的最近日期往前推30天
思路1: 需要进行日期的筛选! */
SELECT tag, retweet_count, retweet_rate     -- 外面这层其实是没必要的
FROM (
    SELECT tag, 
        SUM(if_retweet) AS retweet_count,
        COUNT(if_retweet) AS play_count,
        ROUND(SUM(if_retweet) / COUNT(if_retweet), 3) AS retweet_rate
    FROM tb_user_video_log AS user LEFT JOIN tb_video_info AS video ON user.video_id = video.video_id
    -- WHERE start_time >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)        -- 日期筛选, 这样子是从今天开始算
    WHERE DATE(start_time) >= (SELECT DATE_SUB(MAX(start_time), INTERVAL 30 DAY) FROM tb_user_video_log)    -- 从最近的日期开始算
    -- WHERE DATEDIFF(DATE((select max(start_time) FROM tb_user_video_log)), DATE(a.start_time)) <= 29  -- 用 DATEDIFF 也可以!
    GROUP BY tag
    ORDER BY retweet_rate DESC
) AS tmp2;


/* SQL159 每个创作者每月的涨粉率及截止当前的总粉丝量
问题：计算2021年里每个创作者每月的涨粉率及截止当月的总粉丝量
注：
涨粉率=(加粉量 - 掉粉量) / 播放量。结果按创作者ID、总粉丝量升序排序。
if_follow-是否关注为1表示用户观看视频中关注了视频创作者，为0表示此次互动前后关注状态未发生变化，为2表示本次观看过程中取消了关注。 */



