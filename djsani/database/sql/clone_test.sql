DELETE
FROM
    cc_student_medical_manager
WHERE
    created_at > MDY(4,  1, 2015);

DELETE
FROM
    cc_student_medical_history
WHERE
    created_at > MDY(4,  1, 2015);

DELETE
FROM
    cc_athlete_medical_history
WHERE
    created_at > MDY(4,  1, 2015);

DELETE
FROM
    cc_student_health_insurance
WHERE
    created_at > MDY(4,  1, 2015);

SELECT
    *
FROM
    train:cc_student_health_insurance
WHERE
    college_id=1346599;


SELECT
    *
FROM
    train:cc_student_medical_history
WHERE
    college_id=1346599;

SELECT
    *
FROM
    train:cc_student_medical_manager
WHERE
    college_id=1346599;

SELECT
    *
FROM
    train:cc_student_health_insurance
WHERE
    college_id=1346599;

SELECT
    *
FROM
    train:cc_athlete_sicklecell_waiver
WHERE
    college_id=1346599;
