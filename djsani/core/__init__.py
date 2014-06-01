STUDENTS_ALPHA = """
SELECT UNIQUE
    id_rec.lastname, id_rec.firstname, id_rec.id,
    cc_student_medical_manager.athlete,
    cc_student_medical_manager.sports,
    cc_student_medical_manager.cc_student_medical_history,
    cc_student_medical_manager.cc_student_health_insurance,
    cc_student_medical_manager.cc_student_meni_waiver,
    cc_student_medical_manager.cc_athlete_medical_history,
    cc_student_medical_manager.cc_athlete_privacy_waiver,
    cc_student_medical_manager.cc_athlete_reporting_waiver,
    cc_student_medical_manager.cc_athlete_risk_waiver,
    cc_student_medical_manager.cc_athlete_sicklecell_waiver,
    cc_athlete_sicklecell_waiver.waive,
    cc_athlete_sicklecell_waiver.proof,
    cc_athlete_sicklecell_waiver.results
FROM
    id_rec
INNER JOIN
    prog_enr_rec ON  id_rec.id = prog_enr_rec.id
LEFT JOIN
    cc_student_medical_manager ON id_rec.id = cc_student_medical_manager.cid
LEFT JOIN
    cc_athlete_sicklecell_waiver ON id_rec.id = cc_athlete_sicklecell_waiver.cid
LEFT JOIN
    stu_acad_rec ON  id_rec.id = stu_acad_rec.id
WHERE
    prog_enr_rec.subprog
NOT IN ("UWPK","RSBD","SLS","PARA","MSW","KUSD","ENRM","CONF","CHWK")
AND prog_enr_rec.lv_date IS NULL
AND prog_enr_rec.acst
IN ("GOOD","LOC","PROB","PROC","PROR","READ","RP","SAB","SHAC","SHOC")
AND stu_acad_rec.sess IN ("RA","RC","AM","GC","PC","TC")
AND stu_acad_rec.reg_hrs > 0
"""

#AND prog_enr_rec.cl IN  ("FF","FR","SO","JR","SR","GR","NM")

STUDENT_VITALS = """
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
"""

# IDs must be unique pattern that does not repeat in any other
# item e.g 25 & 250 will not work.
SPORTS = (
    ("0","----Select Sport----"),
    ("","----Men's sports----"),
    ("15","Baseball"),
    ("25","Basketball"),
    ("35","Cross Country"),
    ("45","Football"),
    ("55","Golf"),
    ("65","Lacrosse"),
    ("75","Soccer"),
    ("85","Swimming"),
    ("95","Tennis"),
    ("105","Track &amp; Field"),
    ("120","Volleyball"),
    ("","----Women's sports----"),
    ("200","Basketball"),
    ("210","Cross Country"),
    ("220","Golf"),
    ("230","Lacrosse"),
    ("240","Soccer"),
    ("260","Softball"),
    ("270","Swimming"),
    ("280","Tennis"),
    ("290","Track &amp; Field"),
    ("300","Volleyball"),
    ("305","Water Polo")
)
