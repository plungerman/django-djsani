SELECT
    UNIQUE
    CASE
        WHEN
            NVL(UPPER(stu_serv_rec.bldg), '') = 'CMTR'
        OR
            NVL(stu_serv_rec.bldg, '') = 'undc'
        OR
            NVL(UPPER(stu_serv_rec.bldg), '') = ''
        THEN
            'Commuter'
        ELSE
            'Resident'
        END
    AS
        residency_status,
    id_rec.lastname, id_rec.firstname, id_rec.id,
    cc_student_medical_manager.id as manid,
    cc_student_medical_manager.created_at,
    cc_student_medical_manager.athlete,
    cc_student_medical_manager.sitrep,
    cc_student_health_insurance.primary_policy_type,
    cc_student_health_insurance.primary_company,
    cc_student_health_insurance.secondary_policy_type,
    cc_student_health_insurance.secondary_company
FROM
    id_rec
INNER JOIN
    prog_enr_rec ON  id_rec.id = prog_enr_rec.id
LEFT JOIN
    stu_acad_rec    ON  id_rec.id   =   stu_acad_rec.id
LEFT JOIN
    stu_serv_rec    ON  id_rec.id   =   stu_serv_rec.id
LEFT JOIN
    cc_student_medical_manager ON id_rec.id = cc_student_medical_manager.college_id
    AND
        cc_student_medical_manager.created_at > DATE('2016-06-01')
LEFT JOIN
    cc_student_health_insurance
  ON
    cc_student_medical_manager.id = cc_student_health_insurance.manager_id
WHERE
    prog_enr_rec.subprog NOT IN  ("UWPK","RSBD","SLS","PARA","MSW","KUSD","ENRM","CONF","CHWK")
AND
    prog_enr_rec.lv_date IS  NULL
AND
    stu_acad_rec.sess IN  ("RA","RC","AM","GC","PC","TC","GD","GA","GC")
AND
    stu_serv_rec.yr = "2017"
AND
    stu_serv_rec.sess = "RC"
ORDER BY
    lastname
