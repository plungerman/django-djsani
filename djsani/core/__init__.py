STUDENTS_ALPHA = """
SELECT UNIQUE
id_rec.lastname, id_rec.firstname, id_rec.id
FROM
    id_rec
INNER JOIN  prog_enr_rec ON  id_rec.id = prog_enr_rec.id
LEFT JOIN   stu_acad_rec ON  id_rec.id = stu_acad_rec.id
WHERE
    prog_enr_rec.subprog
NOT IN ("UWPK","RSBD","SLS","PARA","MSW","KUSD","ENRM","CONF","CHWK")
AND prog_enr_rec.lv_date IS NULL
AND prog_enr_rec.cl IN ("FF","FR")
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
    id_rec.zip, id_rec.ctry, id_rec.phone, cvid_rec.ldap_name
FROM
    id_rec
LEFT JOIN
    cvid_rec on id_rec.id = cvid_rec.cx_id
WHERE
    id_rec.id =
"""

STUDENT_HEALTH_INSURANCE = """
SELECT * FROM student_health_insurance WHERE cid =
"""

STUDENT_MEDICAL_HISTORY = """
SELECT * FROM student_medical_history WHERE cid =
"""
ATHLETE_MEDICAL_HISTORY = """
SELECT * FROM athlete_medical_history WHERE cid =
"""
SPORTS = (
    ("0","----Select Sport----"),
    ("","----Men's sports----"),
    ("Men's Baseball","Baseball"),
    ("Men's Basketball","Basketball"),
    ("Men's Cross Country","Cross Country"),
    ("Men's Football","Football"),
    ("Men's Golf","Golf"),
    ("Men's Lacrosse","Lacrosse"),
    ("Men's Soccer","Soccer"),
    ("Men's Swimming","Swimming"),
    ("Men's Tennis","Tennis"),
    ("Men's Track &amp; Field","Track &amp; Field"),
    ("Men's Volleyball","Volleyball"),
    ("","----Women's sports----"),
    ("Women's Basketball","Basketball"),
    ("Women's Cross Country","Cross Country"),
    ("Women's Golf","Golf"),
    ("Women's Lacrosse","Lacrosse"),
    ("Women's Soccer","Soccer"),
    ("Women's Softball","Softball"),
    ("Women's Swimming","Swimming"),
    ("Women's Tennis","Tennis"),
    ("Women's Track &amp; Field","Track &amp; Field"),
    ("Women's Volleyball","Volleyball"),
    ("Women's Water Polo","Water Polo")
)
