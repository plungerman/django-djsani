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
    profile_rec.birth_date,
    cc_student_medical_manager.id as manid,
    cc_student_medical_manager.created_at,
    cc_student_medical_manager.staff_notes,
    cc_student_medical_manager.athlete,
    cc_student_medical_manager.sitrep,
    cc_student_medical_manager.emergency_contact,
    cc_student_medical_manager.sports,
    cc_student_medical_manager.medical_consent_agreement,
    cc_student_medical_manager.physical_evaluation_1,
    cc_student_medical_manager.physical_evaluation_2,
    cc_student_medical_manager.cc_student_medical_history,
    cc_student_medical_manager.cc_student_health_insurance,
    cc_student_medical_manager.cc_student_meni_waiver,
    cc_student_medical_manager.cc_student_immunization,
    cc_student_medical_manager.cc_athlete_medical_history,
    cc_student_medical_manager.cc_athlete_privacy_waiver,
    cc_student_medical_manager.cc_athlete_reporting_waiver,
    cc_student_medical_manager.cc_athlete_risk_waiver,
    cc_student_medical_manager.cc_athlete_sicklecell_waiver,
    cc_student_health_insurance.primary_policy_type,
    cc_athlete_sicklecell_waiver.updated_at,
    cc_athlete_sicklecell_waiver.waive,
    cc_athlete_sicklecell_waiver.proof,
    cc_athlete_sicklecell_waiver.results,
    cc_athlete_sicklecell_waiver.results_file
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
LEFT JOIN
    cc_student_medical_manager ON id_rec.id = cc_student_medical_manager.college_id
    AND
        cc_student_medical_manager.created_at > DATE("2017-06-01")
LEFT JOIN
    cc_student_health_insurance
  ON
    cc_student_medical_manager.id = cc_student_health_insurance.manager_id
LEFT JOIN
    cc_athlete_sicklecell_waiver ON id_rec.id = cc_athlete_sicklecell_waiver.college_id
    AND
        (cc_athlete_sicklecell_waiver.proof = 1 or cc_athlete_sicklecell_waiver.created_at > DATE("2017-06-01"))
WHERE
    prog_enr_rec.subprog NOT IN  ("UWPK","RSBD","SLS","PARA","MSW","KUSD","ENRM","CONF","CHWK")
AND
    prog_enr_rec.lv_date IS  NULL
AND
    stu_acad_rec.sess IN  ("RA","RC","AM","GC","PC","TC","GD","GA","GC")
AND
    stu_serv_rec.yr = year(CURRENT)
AND
    stu_serv_rec.sess =
  CASE
    WHEN month(CURRENT) > 7 THEN "RA"
    ELSE "RC"
  END
AND
    prog_enr_rec.cl IN ("FN","FF","FR","UT","PFF")
ORDER BY
    lastname
