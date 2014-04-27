/* table athlete_risk_waiver */

CREATE TABLE athlete_risk_waiver
(
    /* core */
    id                      SERIAL NOT NULL,
    cid                     INTEGER NOT NULL,
    created_at DATETIME YEAR TO SECOND DEFAULT CURRENT YEAR TO SECOND NOT NULL,
    updated_at DATETIME YEAR TO SECOND DEFAULT CURRENT YEAR TO SECOND NOT NULL,
    /* waiver fields */
    agree                   BOOLEAN,
    /* constraints */
    PRIMARY KEY (id),
    FOREIGN KEY (cid) REFERENCES id_rec (id)
);
