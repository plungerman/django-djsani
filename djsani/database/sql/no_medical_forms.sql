SELECT
    UNIQUE
    CASE
        WHEN
            NVL(UPPER(stu_serv_rec.bldg), '') = 'CMTR'
        OR
            NVL(UPPER(stu_serv_rec.bldg), '') = ''
        THEN
            'Commuter'
        ELSE
            'Resident'
        END
    AS
        residency_status,
    cvid_rec.ldap_name,
    id_rec.lastname, id_rec.firstname, id_rec.id,
    profile_rec.birth_date,
    cc_student_medical_manager.id as manid,
    cc_student_medical_manager.athlete,
    cc_student_medical_manager.sitrep,
    cc_student_medical_manager.emergency_contact,
    cc_student_medical_manager.sports,
    cc_student_medical_manager.cc_student_medical_history,
    cc_student_medical_manager.cc_student_health_insurance,
    cc_student_medical_manager.cc_student_meni_waiver,
    cc_student_medical_manager.cc_student_immunization,
    cc_student_medical_manager.cc_athlete_medical_history,
    cc_student_medical_manager.cc_athlete_privacy_waiver,
    cc_student_medical_manager.cc_athlete_reporting_waiver,
    cc_student_medical_manager.cc_athlete_risk_waiver,
    cc_student_medical_manager.cc_athlete_sicklecell_waiver,
    cc_athlete_sicklecell_waiver.updated_at,
    cc_athlete_sicklecell_waiver.waive,
    cc_athlete_sicklecell_waiver.proof,
    cc_athlete_sicklecell_waiver.results
FROM
    id_rec
INNER JOIN
    prog_enr_rec ON  id_rec.id = prog_enr_rec.id
LEFT JOIN
    stu_serv_rec  ON  id_rec.id = stu_serv_rec.id
LEFT JOIN
    stu_acad_rec    ON  id_rec.id   =   stu_acad_rec.id
LEFT JOIN
    cvid_rec     ON  id_rec.id = cvid_rec.cx_id
LEFT JOIN
    profile_rec  ON  id_rec.id = profile_rec.id
LEFT JOIN
    cc_student_medical_manager ON id_rec.id = cc_student_medical_manager.college_id
    AND
        cc_student_medical_manager.created_at > DATE('06-01-15')
LEFT JOIN
    cc_athlete_sicklecell_waiver ON id_rec.id = cc_athlete_sicklecell_waiver.college_id
    AND
        (cc_athlete_sicklecell_waiver.proof = 1 or cc_athlete_sicklecell_waiver.created_at > DATE('06-01-15'))
WHERE
    prog_enr_rec.subprog    NOT IN  ("UWPK","RSBD","SLS","PARA","MSW","KUSD","ENRM","CONF","CHWK")
    AND prog_enr_rec.lv_date    IS  NULL
    AND prog_enr_rec.acst   IN  ("GOOD","LOC","PROB","PROC","PROR","READ","RP","SAB","SHAC","SHOC","TRAD")
    AND stu_serv_rec.add_date > TO_DATE('2015-05-01', '%Y-%m-%d')
    AND stu_serv_rec.add_date IS NOT NULL
    AND stu_acad_rec.sess   IN  ("RA","RC","AM","GC","PC","TC")
    AND stu_acad_rec.reg_hrs    >   0
    AND cc_student_medical_manager.id IS NULL
ORDER BY lastname;
