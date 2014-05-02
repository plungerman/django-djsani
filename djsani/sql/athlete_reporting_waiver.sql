/* table athlete_reporting_waiver */

CREATE TABLE athlete_reporting_waiver
(
    /* core */
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    cid                     varchar(12) NOT NULL,
    created_at DATETIME NOT NULL,
    /* waiver fields */
    agree                   BOOLEAN
);
