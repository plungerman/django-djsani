/* table cc_student_meni_waiver */

CREATE TABLE cc_student_meni_waiver
(
    /* core */
    id                      INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    cid                     INT(11) NOT NULL,
    created_at              DATETIME NOT NULL,
    /* waiver fields */
    agree                   BOOLEAN
);
