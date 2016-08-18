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
    id_rec.lastname, id_rec.firstname, id_rec.middlename, id_rec.id,
    profile_rec.birth_date
FROM
    id_rec
INNER JOIN
    prog_enr_rec ON  id_rec.id = prog_enr_rec.id
LEFT JOIN
    stu_acad_rec    ON  id_rec.id   =   stu_acad_rec.id
LEFT JOIN
    stu_serv_rec    ON  id_rec.id   =   stu_serv_rec.id
LEFT JOIN
    profile_rec  ON  id_rec.id = profile_rec.id
WHERE
    prog_enr_rec.subprog NOT IN  ("UWPK","RSBD","SLS","PARA","MSW","KUSD","ENRM","CONF","CHWK")
AND
    prog_enr_rec.lv_date IS  NULL
AND
    stu_acad_rec.sess IN  ("RA","RC","AM","GC","PC","TC")

        AND stu_serv_rec.yr = "2016"
        AND stu_serv_rec.sess = "RA"
        AND prog_enr_rec.cl IN ("FN","FF","FR","UT")
        ORDER BY lastname
