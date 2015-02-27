/* table cc_student_medical_manager */

CREATE TABLE cc_student_medical_manager
(
    /* core */
    id                          INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    college_id                  INT(11) NOT NULL,
    created_at                  DATETIME NOT NULL,
    athlete                     TINYINT(1),
    sports                      VARCHAR(255),
    /* forms and waivers */
    cc_student_medical_history      TINYINT(1),
    cc_student_health_insurance     TINYINT(1),
    cc_student_meni_waiver          TINYINT(1),
    cc_athlete_medical_history      TINYINT(1),
    cc_athlete_privacy_waiver       TINYINT(1),
    cc_athlete_reporting_waiver     TINYINT(1),
    cc_athlete_risk_waiver          TINYINT(1),
    cc_athlete_sicklecell_waiver    TINYINT(1)
);
