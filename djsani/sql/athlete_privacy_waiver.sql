/* table athlete_sicklecell_waiver */

CREATE TABLE athlete_sicklecell_waiver
(
    /* core */
    id                      SERIAL NOT NULL,
    cid                     INTEGER NOT NULL,
    created_at DATETIME YEAR TO SECOND DEFAULT CURRENT YEAR TO SECOND NOT NULL,
    updated_at DATETIME YEAR TO SECOND DEFAULT CURRENT YEAR TO SECOND NOT NULL,
    /* waiver fields */
    ncaa_tool               BOOLEAN,
    medical_insurance       BOOLEAN,
    news_media              BOOLEAN,
    parents_guardians       BOOLEAN,
    disclose_records        BOOLEAN,
    /* constraints */
    PRIMARY KEY (id),
    FOREIGN KEY (cid) REFERENCES id_rec (id)
);
