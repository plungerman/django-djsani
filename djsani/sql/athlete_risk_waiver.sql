/* table athlete_risk_waiver */

CREATE TABLE athlete_risk_waiver
(
    /* core */
    id                      INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    cid                     VARCHAR(12) NOT NULL,
    created_at              DATETIME NOT NULL,
    /* waiver fields */
    agree                   BOOLEAN
);
