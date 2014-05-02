/* table athlete_privacy_waiver */

CREATE TABLE athlete_privacy_waiver
(
    /* core */
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    cid                     varchar(12) NOT NULL,
    created_at DATETIME NOT NULL,
    /* waiver fields */
    ncaa_tool               BOOLEAN,
    medical_insurance       BOOLEAN,
    news_media              BOOLEAN,
    parents_guardians       BOOLEAN,
    disclose_records        BOOLEAN
);
