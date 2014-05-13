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
    profile_rec.birth_date
FROM
    id_rec
LEFT JOIN
    cvid_rec     ON  id_rec.id = cvid_rec.cx_id
LEFT JOIN
    profile_rec  ON  id_rec.id = profile_rec.id
WHERE
    id_rec.id =
"""

SPORTS = (
    ("0","----Select Sport----"),
    ("","----Men's sports----"),
    ("10","Baseball"),
    ("20","Basketball"),
    ("30","Cross Country"),
    ("40","Football"),
    ("50","Golf"),
    ("60","Lacrosse"),
    ("70","Soccer"),
    ("80","Swimming"),
    ("90","Tennis"),
    ("100","Track &amp; Field"),
    ("110","Volleyball"),
    ("","----Women's sports----"),
    ("200","Basketball"),
    ("210","Cross Country"),
    ("220","Golf"),
    ("230","Lacrosse"),
    ("240","Soccer"),
    ("250","Softball"),
    ("260","Swimming"),
    ("270","Tennis"),
    ("280","Track &amp; Field"),
    ("290","Volleyball"),
    ("300","Water Polo")
)
