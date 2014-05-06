/* table student_medical_manager */

CREATE TABLE student_medical_manager
(
    /* core */
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    cid                     varchar(12) NOT NULL,
    created_at DATETIME NOT NULL,
    athlete                 BOOLEAN,
    /* forms and waivers */
    student_medical_history BOOLEAN not null default 0,
    athlete_medical_history BOOLEAN not null default 0,
    health_insurance        BOOLEAN not null default 0,
    sicklecell              BOOLEAN not null default 0,
    privacy                 BOOLEAN not null default 0,
    risk                    BOOLEAN not null default 0,
    cciw_reporting          BOOLEAN not null default 0
);
