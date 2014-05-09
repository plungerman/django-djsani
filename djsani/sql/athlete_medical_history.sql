/* table athlete_medical_history */

CREATE TABLE athlete_medical_history
(
    /* core */
    id                      INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    cid                     VARCHAR(12) NOT NULL,
    created_at              DATETIME NOT NULL,
    /* medical questions/explanations */
    exertional_syncope      VARCHAR(255),
    heat_illness            VARCHAR(255),
    intense_chest_pain      VARCHAR(255),
    sickle_cell_trait       VARCHAR(255),
    /* Head and Neck Injury */
    concussion              VARCHAR(255),
    suspected_concussion    VARCHAR(255),
    head_injuries           VARCHAR(255),
    season_ending           VARCHAR(255),
    cervical_injury         VARCHAR(255),
    stinger_injury          VARCHAR(255),
    neurologist_treatment   VARCHAR(255),
    spine_injury            VARCHAR(255),
    history_headaches       VARCHAR(255),
    history_migraines       VARCHAR(255),
    /* Torso Injury */
    abdomen_injury          VARCHAR(255),
    rib_injury              VARCHAR(255),
    lumbar_injury           VARCHAR(255),
    /* Upper Extremity Injury */
    shoulder_fracture       VARCHAR(255),
    shoulder_dislocation    VARCHAR(255),
    shoulder_muscle         VARCHAR(255),
    labrum_injury           VARCHAR(255),
    forearm_injury          VARCHAR(255),
    elbow_injury            VARCHAR(255),
    wrist_injury            VARCHAR(255),
    finger_injury           VARCHAR(255),
    /* Lower Extremity Injury */
    hip_pelvis              VARCHAR(255),
    hamstring               VARCHAR(255),
    quadriceps              VARCHAR(255),
    thigh_other             VARCHAR(255),
    knee_ligaments          VARCHAR(255),
    meniscus                VARCHAR(255),
    patella                 VARCHAR(255),
    knee_other              VARCHAR(255),
    shin_spints             VARCHAR(255),
    stress_fractures        VARCHAR(255),
    compartment_syndrome    VARCHAR(255),
    lower_leg_other         VARCHAR(255),
    ankle_fracture          VARCHAR(255),
    ankle_sprain            VARCHAR(255),
    foot                    VARCHAR(255),
    toe                     VARCHAR(255),
    /* Ears, Eyes, Dental */
    glasses                 VARCHAR(255),
    contact_lenses          VARCHAR(255),
    hearing_aids            VARCHAR(255),
    dental_appliances       VARCHAR(255),
    /* Additional Medical Information */
    previous_year_change    VARCHAR(255),
    physician_prohibition   VARCHAR(255),
    other_information       VARCHAR(255),
    supplements             VARCHAR(255),
    /* Female Athletes Only */
    menstrual_cycle         VARCHAR(255)
);
