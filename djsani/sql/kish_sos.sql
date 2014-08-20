SELECT
    IDrec.id, IDrec.firstname, IDrec.lastname
FROM
    id_rec  IDrec
INNER JOIN
    stu_serv_rec    SRVrec  ON  IDrec.id    =   SRVrec.id
AND
    SRVrec.yr   =   2014
AND
    SRVrec.sess =   'RA'
LEFT JOIN
    aa_rec  ENS ON  IDrec.id    =   ENS.id
AND
    ENS.aa  =   'ENS'
WHERE
    ENS.aa_no   IS  NULL
ORDER BY
    lastname, firstname
