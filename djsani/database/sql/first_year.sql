SELECT
    id_rec.lastname, id_rec.firstname, id_rec.id,
    id_rec.addr_line1, id_rec.addr_line2, id_rec.city, id_rec.st,
    id_rec.zip, id_rec.ctry, id_rec.phone, cvid_rec.ldap_name,
    adm_rec.plan_enr_sess,adm_rec.plan_enr_yr,
    cc_student_medical_manager.athlete,
    profile_rec.birth_date
FROM
    id_rec
LEFT JOIN
    adm_rec     ON  id_rec.id = adm_rec.id
LEFT JOIN
    cvid_rec     ON  id_rec.id = cvid_rec.cx_id
LEFT JOIN
    cc_student_medical_manager ON  id_rec.id = cc_student_medical_manager.cid
LEFT JOIN
    profile_rec  ON  id_rec.id = profile_rec.id
WHERE
    adm_rec.plan_enr_yr="2014"
AND
    adm_rec.plan_enr_sess="RA"
AND
    id_rec.lastname="Garcia"
