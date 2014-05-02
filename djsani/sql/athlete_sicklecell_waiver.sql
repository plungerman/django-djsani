/* table athlete_sicklecell_waiver */

CREATE TABLE athlete_sicklecell_waiver
(
    /* core */
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    cid                     varchar(12) NOT NULL,
    created_at DATETIME NOT NULL,
    /* waiver fields */
    waive                   BOOLEAN,
    proof                   BOOLEAN,
    results                 VARCHAR(64)
);
