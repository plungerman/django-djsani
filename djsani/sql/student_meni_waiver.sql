/* table student_meni_waiver */

CREATE TABLE student_meni_waiver
(
    /* core */
    id                      INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    cid                     VARCHAR(12) NOT NULL,
    created_at              DATETIME NOT NULL,
    /* waiver fields */
    agree                   BOOLEAN
);
