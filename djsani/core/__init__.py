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

STUDENT = """
SELECT
    id_rec.lastname, id_rec.firstname, id_rec.id
FROM
    id_rec
WHERE
    id_rec.id =
"""

INSURANCE = """
SELECT * FROM student_health_insurance WHERE cid =
"""

MEDICAL = """
SELECT * FROM student_medical_history WHERE cid =
"""

FIELDS = [
    'aa','beg_date','end_date','line1','line2','line3',
    'phone','phone_ext','cell_carrier','opt_out'
]

CODES = ['MIS1','MIS2','MIS3','ICE','ICE2','ENS']
