SELECT
    COUNT(*)
FROM
    invl_table IT
INNER JOIN
    involve_rec INR
ON
    TRIM(IT.invl) = TRIM(INR.invl)
AND
    IT.sanc_sport = 'Y'
WHERE
    TODAY BETWEEN IT.active_date AND NVL(IT.inactive_date, TODAY)
AND
    TODAY < INR.end_date
AND
    INR.id =
HAVING COUNT(*)>0
