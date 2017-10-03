SELECT
    college_id, created_at,
    COUNT(*) count
FROM
    cc_student_health_insurance
WHERE
    created_at > DATE('2017-06-01')
GROUP BY
    college_id, created_at
HAVING
    count(*) > 1
