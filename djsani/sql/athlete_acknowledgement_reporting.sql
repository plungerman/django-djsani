/* table athlete_acknowledgement_reporting */

CREATE TABLE athlete_acknowledgement_reporting
(
    /* core */
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    cid                     INT NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    /* waiver fields */
    agree                   BOOLEAN
);
