/* table athlete_sicklecell_waiver */

CREATE TABLE athlete_sicklecell_waiver
(
    /* core */
    id                      SERIAL NOT NULL,
    cid                     INTEGER NOT NULL,
    created_at DATETIME YEAR TO SECOND DEFAULT CURRENT YEAR TO SECOND NOT NULL,
    updated_at DATETIME YEAR TO SECOND DEFAULT CURRENT YEAR TO SECOND NOT NULL,
    /* waiver fields */
    waive                   BOOLEAN,
    proof                   BOOLEAN,
    results                 VARCHAR(64),
    /* constraints */
    PRIMARY KEY (id),
    FOREIGN KEY (cid) REFERENCES id_rec (id)
);
