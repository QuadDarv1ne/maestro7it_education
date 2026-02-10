# Write your MySQL query statement below
SELECT
    id,
    MAX(IF(month = 'Jan', revenue, NULL)) AS Jan_Revenue,
    MAX(IF(month = 'Feb', revenue, NULL)) AS Feb_Revenue,
    MAX(IF(month = 'Mar', revenue, NULL)) AS Mar_Revenue,
    MAX(IF(month = 'Apr', revenue, NULL)) AS Apr_Revenue,
    MAX(IF(month = 'May', revenue, NULL)) AS May_Revenue,
    MAX(IF(month = 'Jun', revenue, NULL)) AS Jun_Revenue,
    MAX(IF(month = 'Jul', revenue, NULL)) AS Jul_Revenue,
    MAX(IF(month = 'Aug', revenue, NULL)) AS Aug_Revenue,
    MAX(IF(month = 'Sep', revenue, NULL)) AS Sep_Revenue,
    MAX(IF(month = 'Oct', revenue, NULL)) AS Oct_Revenue,
    MAX(IF(month = 'Nov', revenue, NULL)) AS Nov_Revenue,
    MAX(IF(month = 'Dec', revenue, NULL)) AS Dec_Revenue
FROM Department
GROUP BY id;