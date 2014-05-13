/* table student_medical_manager */

CREATE TABLE student_medical_manager
(
    /* core */
    id                          INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    cid                         VARCHAR(12) NOT NULL,
    created_at                  DATETIME NOT NULL,
    athlete                     BOOLEAN,
    sports                      VARCHAR(255),
    /* forms and waivers */


    student_medical_history     BOOLEAN not null default 0,
    student_health_insurance    BOOLEAN not null default 0,
    student_meni_waiver         BOOLEAN not null default 0,
    athlete_medical_history     BOOLEAN not null default 0,
    athlete_privacy_waiver      BOOLEAN not null default 0,
    athlete_reporting_waiver    BOOLEAN not null default 0,
    athlete_risk_waiver         BOOLEAN not null default 0,
    athlete_sicklecell_waiver   BOOLEAN not null default 0,
);
