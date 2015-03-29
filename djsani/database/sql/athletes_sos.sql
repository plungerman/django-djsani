SELECT
    IDrec.lastname, IDrec.firstname, IDrec.id, cc_student_medical_manager.athlete,cc_student_medical_manager.sports
FROM
    id_rec  IDrec
INNER JOIN
    stu_serv_rec    SRVrec  ON  IDrec.id    =   SRVrec.id
INNER JOIN
    cc_student_medical_manager ON IDrec.id = cc_student_medical_manager.college_id
AND
    SRVrec.yr   =   2014
AND
    SRVrec.sess =   'RA'
AND
    cc_student_medical_manager.athlete=1
LEFT JOIN
    aa_rec  ENS ON  IDrec.id    =   ENS.id
AND
    ENS.aa  =   'ENS'
WHERE
    ENS.aa_no   IS  NULL
ORDER BY lastname, firstname;
