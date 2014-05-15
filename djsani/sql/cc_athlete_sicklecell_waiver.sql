/* table cc_athlete_sicklecell_waiver */

CREATE TABLE cc_athlete_sicklecell_waiver
(
    /* core */
    id                      INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    cid                     INT(11) NOT NULL,
    created_at              DATETIME NOT NULL,
    /* waiver fields */
    waive                   TINYINT(1),
    proof                   TINYINT(1),
    results                 VARCHAR(64)
);
