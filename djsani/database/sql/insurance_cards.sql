SELECT
    UNIQUE
    id_rec.lastname, id_rec.firstname, cc_student_health_insurance.created_at,
    cc_student_health_insurance.primary_card_front,
    id_rec.id, id_rec.ss_no,
    id_rec.addr_line1, id_rec.addr_line2, id_rec.city, id_rec.st,
    id_rec.zip, id_rec.ctry, id_rec.phone,
    cc_student_medical_manager.id as manid,
    cc_student_medical_manager.sitrep,
    cc_student_medical_manager.athlete,
    profile_rec.birth_date,
    profile_rec.sex,
    mobile_rec.phone as mobile,
    mobile_rec.phone as mobile
FROM
    id_rec
LEFT JOIN
    cc_student_medical_manager ON id_rec.id = cc_student_medical_manager.college_id
LEFT JOIN
    cc_student_health_insurance ON cc_student_medical_manager.id = cc_student_health_insurance.manager_id
LEFT JOIN
    profile_rec  ON  id_rec.id = profile_rec.id
LEFT JOIN
    aa_rec as mobile_rec on
    (id_rec.id = mobile_rec.id AND mobile_rec.aa = "ENS")
WHERE
    cc_student_medical_manager.athlete = 1
and cc_student_medical_manager.cc_student_health_insurance =1
and cc_student_health_insurance.opt_out != 1
and cc_student_health_insurance.primary_card_front is null
and cc_student_health_insurance.created_at > DATE("2016-05-01");
