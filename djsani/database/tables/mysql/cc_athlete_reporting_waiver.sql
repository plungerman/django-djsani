/* table cc_athlete_reporting_waiver */

CREATE TABLE cc_athlete_reporting_waiver
(
    /* core */
    id                      INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    cid                     INT(11) NOT NULL,
    created_at              DATETIME NOT NULL,
    /* waiver fields */
    agree                   TINYINT(1)
);
