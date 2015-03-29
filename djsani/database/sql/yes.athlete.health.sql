SELECT
    id_rec.lastname, id_rec.firstname,
    cvid_rec.ldap_name,
    id_rec.id,
    exertional_syncope, heat_illness, intense_chest_pain  , sickle_cell_trait   , concussion  , suspected_concussion, head_injuries   , season_ending   , cervical_injury , stinger_injury  , neurologist_treatment   , spine_injury, history_headaches   , history_migraines   , abdomen_injury  , rib_injury  , lumbar_injury   , shoulder_fracture   , shoulder_dislocation, shoulder_muscle , labrum_injury   , forearm_injury  , elbow_injury, wrist_injury, finger_injury   , hip_pelvis  , hamstring   , quadriceps  , thigh_other , knee_ligaments  , meniscus, patella , knee_other  , shin_splints, stress_fractures, compartment_syndrome, lower_leg_other , ankle_fracture  , ankle_sprain, foot, toe , glasses , contact_lenses  , hearing_aids, dental_appliances   , previous_year_change, physician_prohibition   , other_information   , supplements , menstrual_cycle
FROM
    id_rec
LEFT JOIN
    cvid_rec     ON  id_rec.id = cvid_rec.cx_id
LEFT JOIN
    cc_athlete_medical_history ON  id_rec.id = cc_athlete_medical_history.college_id
LEFT JOIN
    cc_student_medical_manager ON  id_rec.id = cc_student_medical_manager.college_id
WHERE
    cc_student_medical_manager.cc_athlete_medical_history = 1
ORDER BY
    id_rec.lastname
