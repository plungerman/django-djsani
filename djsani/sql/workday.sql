SELECT
    UNIQUE
    CASE
        WHEN NVL(stu_serv_rec.intend_hsg, 'C') IN ('C', 'O') THEN 'Commuter' ELSE 'Resident'
    END AS residency_status,
    id_rec.id, id_rec.lastname, id_rec.firstname, id_rec.middlename,
    id_rec.addr_line1, id_rec.addr_line2, id_rec.city, id_rec.st,
    id_rec.zip, id_rec.ctry, id_rec.phone,
    TRIM(cvid_rec.ldap_name) as ldap_name,
    profile_rec.birth_date,
    profile_rec.sex,
    prog_enr_rec.cl,
    mobile_rec.phone as mobile
FROM
    id_rec
INNER JOIN
    prog_enr_rec
ON
    id_rec.id = prog_enr_rec.id
LEFT JOIN
    cvid_rec
ON
    id_rec.id = cvid_rec.cx_id
LEFT JOIN
    profile_rec
ON
    id_rec.id = profile_rec.id
LEFT JOIN
    stu_serv_rec
ON
    id_rec.id = stu_serv_rec.id
LEFT JOIN
    stu_acad_rec
ON
    id_rec.id = stu_acad_rec.id
LEFT JOIN
    aa_rec as mobile_rec
ON
    (id_rec.id = mobile_rec.id AND mobile_rec.aa = "ENS")
WHERE
    prog_enr_rec.subprog
NOT IN
    ("UWPK","RSBD","SLS","PARA","MSW","KUSD","ENRM","CONF","CHWK")
AND
    prog_enr_rec.lv_date IS NULL
AND
    stu_acad_rec.sess
IN
    ("RA","RC","AM","GC","PC","TC","GD","GA","GC")
AND stu_serv_rec.yr = "2023"
AND stu_serv_rec.sess = "RC"
