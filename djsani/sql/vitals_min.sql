SELECT UNIQUE
    id_rec.lastname, id_rec.firstname, id_rec.id,
    id_rec.zip, id_rec.ctry, id_rec.phone, cvid_rec.ldap_name,
    cvid_rec.ldap_add_date
FROM
    id_rec
LEFT JOIN
    cvid_rec     ON  id_rec.id = cvid_rec.cx_id
WHERE
    id_rec.id =
/*
    id_rec.lastname=""
 */

