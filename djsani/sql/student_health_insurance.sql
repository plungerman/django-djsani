/* table student_health_insurance */

CREATE TABLE student_health_insurance
(
    /* core */
    id                      SERIAL NOT NULL,
    cid                     INTEGER NOT NULL,
    created_at DATETIME YEAR TO SECOND DEFAULT CURRENT YEAR TO SECOND NOT NULL,
    updated_at DATETIME YEAR TO SECOND DEFAULT CURRENT YEAR TO SECOND NOT NULL,
    opt_out                 BOOLEAN NOT NULL,
    second_policy           BOOLEAN NOT NULL,
    /* primary */
    primary_policy_holder   VARCHAR(128),
    primary_dob             DATE,
    primary_company         VARCHAR(128),
    primary_phone           VARCHAR(12),
    primary_member_id       VARCHAR(64),
    primary_group_no        VARCHAR(64),
    primary_policy_type     VARCHAR(128),
    primary_address         VARCHAR(255),
    /* secondary */
    secondary_policy_holder VARCHAR(128),
    secondary_dob           DATE,
    secondary_company       VARCHAR(128),
    secondary_phone         VARCHAR(12),
    secondary_member_id     VARCHAR(64),
    secondary_group_no      VARCHAR(64),
    secondary_policy_type   VARCHAR(128),
    secondary_address       VARCHAR(255),
    /* constraints */
    PRIMARY KEY (id),
    FOREIGN KEY (cid) REFERENCES id_rec (id)
);
