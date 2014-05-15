/* table cc_student_health_insurance */

CREATE TABLE cc_student_health_insurance
(
    /* core */
    id                      INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    cid                     INT(11) NOT NULL,
    created_at              DATETIME NOT NULL,
    opt_out                 TINYINT(1),
    /* primary */
    primary_policy_holder   VARCHAR(128),
    primary_dob             DATE,
    primary_company         VARCHAR(128),
    primary_phone           VARCHAR(12),
    primary_member_id       VARCHAR(64),
    primary_group_no        VARCHAR(64),
    primary_policy_type     VARCHAR(128),
    primary_policy_state    VARCHAR(2),
    primary_address         VARCHAR(255),
    /* secondary */
    secondary_policy_holder VARCHAR(128),
    secondary_dob           DATE,
    secondary_company       VARCHAR(128),
    secondary_phone         VARCHAR(12),
    secondary_member_id     VARCHAR(64),
    secondary_group_no      VARCHAR(64),
    secondary_policy_type   VARCHAR(128),
    secondary_policy_state  VARCHAR(2),
    secondary_address       VARCHAR(255)
);
