SELECT
   TRIM(IT.invl) AS sport_code,
   TRIM(IT.txt) AS sport_name,
   INR.id AS id,
   INR.beg_date,
   INR.end_date
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
   TODAY < NVL(INR.end_date, TODAY)
AND
   INR.id =
