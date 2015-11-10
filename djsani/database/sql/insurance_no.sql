SELECT UNIQUE
    id_rec.lastname, id_rec.firstname,
    cc_student_medical_manager.college_id,
    cc_student_medical_manager.created_at,
    cc_student_health_insurance.opt_out
FROM
    id_rec
LEFT JOIN
    cc_student_medical_manager
  ON
    id_rec.id = cc_student_medical_manager.college_id
LEFT JOIN
    cc_student_health_insurance
  ON
    cc_student_medical_manager.id = cc_student_health_insurance.manager_id
WHERE
    cc_student_health_insurance.opt_out = 1
AND
    cc_student_medical_manager.created_at > "2015-06-01 00:00:00"
ORDER BY
    id_rec.lastname;
