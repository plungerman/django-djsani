SELECT
    college_id, created_at, COUNT(*)
FROM
    cars:cc_student_medical_history
GROUP BY
    college_id, created_at
HAVING
    COUNT(*) > 1;

SELECT
    college_id, created_at, COUNT(*)
FROM
    cars:cc_athlete_medical_history
GROUP BY
    college_id, created_at
HAVING
    COUNT(*) > 1;

SELECT
    college_id, created_at, COUNT(*)
FROM
    cars:cc_athlete_privacy_waiver
GROUP BY
    college_id, created_at
HAVING
    COUNT(*) > 1;

SELECT
    college_id, created_at, COUNT(*)
FROM
    cars:cc_athlete_reporting_waiver
GROUP BY
    college_id, created_at
HAVING
    COUNT(*) > 1;

SELECT
    college_id, created_at, COUNT(*)
FROM
    cars:cc_student_health_insurance
GROUP BY
    college_id, created_at
HAVING
    COUNT(*) > 1;

SELECT
    college_id, created_at, COUNT(*)
FROM
    cars:cc_student_meni_waiver
GROUP BY
    college_id, created_at
HAVING
    COUNT(*) > 1;

/* No dupes */

SELECT
    college_id, created_at, COUNT(*)
FROM
    cars:cc_athlete_risk_waiver
GROUP BY
    college_id, created_at
HAVING
    COUNT(*) > 1;

SELECT
    college_id, created_at, COUNT(*)
FROM
    cars:cc_student_medical_manager
GROUP BY
    college_id, created_at
HAVING
    COUNT(*) > 1;

SELECT
    college_id, created_at, COUNT(*)
FROM
    cars:cc_athlete_sicklecell_waiver
GROUP BY
    college_id, created_at
HAVING
    COUNT(*) > 1;

