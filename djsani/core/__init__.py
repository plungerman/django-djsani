STUDENTS_ALPHA = """
SELECT UNIQUE
    id_rec.lastname, id_rec.firstname, id_rec.id,
    profile_rec.birth_date,
    cc_student_medical_manager.athlete,
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
    cc_athlete_sicklecell_waiver.waive,
    cc_athlete_sicklecell_waiver.proof,
    cc_athlete_sicklecell_waiver.results
FROM
    id_rec
INNER JOIN
    stu_serv_rec  ON  id_rec.id = stu_serv_rec.id
AND
    stu_serv_rec.yr   =   2014
AND
    stu_serv_rec.sess =   'RA'
INNER JOIN
    prog_enr_rec ON  id_rec.id = prog_enr_rec.id
LEFT JOIN
    profile_rec  ON  id_rec.id = profile_rec.id
LEFT JOIN
    cc_student_medical_manager ON id_rec.id = cc_student_medical_manager.college_id
LEFT JOIN
    cc_athlete_sicklecell_waiver ON id_rec.id = cc_athlete_sicklecell_waiver.college_id
"""

GROUP_BY = """
GROUP BY
    lastname, firstname, id_rec.id, athlete, sports,
    cc_student_medical_history, cc_student_health_insurance,
    cc_student_meni_waiver, cc_student_immunization,
    cc_athlete_medical_history, cc_athlete_privacy_waiver,
    cc_athlete_reporting_waiver, cc_athlete_risk_waiver,
    cc_athlete_sicklecell_waiver, waive, proof, results
"""

# original WHERE clause
'''
WHERE
    prog_enr_rec.subprog
NOT IN ("UWPK","RSBD","SLS","PARA","MSW","KUSD","ENRM","CONF","CHWK")
AND prog_enr_rec.acst
IN ("GOOD","LOC","PROB","PROC","PROR","READ","RP","SAB","SHAC","SHOC")
AND stu_acad_rec.sess IN ("RA","RC","AM","GC","PC","TC")
AND stu_acad_rec.reg_hrs > 0
'''
# moved to view method
#AND prog_enr_rec.cl IN  ("FF","FR","SO","JR","SR","GR","NM")

STUDENT_VITALS = """
SELECT
    id_rec.lastname, id_rec.firstname, id_rec.id,
    id_rec.addr_line1, id_rec.addr_line2, id_rec.city, id_rec.st,
    id_rec.zip, id_rec.ctry, id_rec.phone, cvid_rec.ldap_name,
    adm_rec.plan_enr_sess,adm_rec.plan_enr_yr,
    cc_student_medical_manager.athlete, cc_student_medical_manager.sports,
    cc_student_medical_manager.cc_student_immunization,
    cc_student_medical_manager.cc_student_meni_waiver,
    cc_student_medical_manager.cc_athlete_privacy_waiver,
    cc_student_medical_manager.cc_athlete_reporting_waiver,
    cc_student_medical_manager.cc_athlete_risk_waiver,
    cc_student_medical_manager.cc_athlete_sicklecell_waiver,
    cc_athlete_sicklecell_waiver.waive,
    cc_athlete_sicklecell_waiver.proof,
    cc_athlete_sicklecell_waiver.results,
    profile_rec.birth_date,
    mobile_rec.phone as mobile
FROM
    id_rec
LEFT JOIN
    adm_rec     ON  id_rec.id = adm_rec.id
LEFT JOIN
    cvid_rec     ON  id_rec.id = cvid_rec.cx_id
LEFT JOIN
    cc_student_medical_manager ON  id_rec.id = cc_student_medical_manager.college_id
LEFT JOIN
    cc_athlete_sicklecell_waiver ON id_rec.id = cc_athlete_sicklecell_waiver.college_id
LEFT JOIN
    profile_rec  ON  id_rec.id = profile_rec.id
LEFT JOIN
    aa_rec as mobile_rec on
    (id_rec.id = mobile_rec.id AND mobile_rec.aa = "ENS")
"""

# IDs must be unique pattern that does not repeat in any other
# item e.g 25 & 250 will not work.
SPORTS = (
    ("0","----Select Sport----"),
    ("","----Men's sports----"),
    ("15","Men's Baseball"),
    ("25","Men's Basketball"),
    ("35","Men's Cross Country"),
    ("45","Men's Football"),
    ("55","Men's Golf"),
    ("65","Men's Lacrosse"),
    ("75","Men's Soccer"),
    ("85","Men's Swimming"),
    ("95","Men's Tennis"),
    ("105","Men's Track &amp; Field"),
    ("120","Men's Volleyball"),
    ("","----Women's sports----"),
    ("200","Women's Basketball"),
    ("210","Women's Cross Country"),
    ("220","Women's Golf"),
    ("230","Women's Lacrosse"),
    ("240","Women's Soccer"),
    ("260","Women's Softball"),
    ("270","Women's Swimming"),
    ("280","Women's Tennis"),
    ("290","Women's Track &amp; Field"),
    ("300","Women's Volleyball"),
    ("305","Women's Water Polo")
)
