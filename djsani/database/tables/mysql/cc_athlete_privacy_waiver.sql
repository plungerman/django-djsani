/* table cc_athlete_privacy_waiver */

CREATE TABLE cc_athlete_privacy_waiver
(
    /* core */
    id                      INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    cid                     INT(11) NOT NULL,
    created_at              DATETIME NOT NULL,
    /* waiver fields */
    ncaa_tool               TINYINT(1),
    medical_insurance       TINYINT(1),
    news_media              TINYINT(1),
    parents_guardians       TINYINT(1),
    disclose_records        TINYINT(1)
);
