SELECT
    auth_user.id,
    auth_user.first_name,
    auth_user.last_name,
    auth_user.email,
    student_profile.second_name,
    student_profile.alt_name,
    student_profile.status,
    student_profile.birth_date,
    student_profile.adult,
    student_profile.address1,
    student_profile.address2,
    student_profile.city,
    student_profile.state,
    student_profile.postal_code,
    student_profile.country,
    student_profile.phone,
    student_profile.gender,
    student_profile.class_year,
    student_profile.residency,
    student_medical_manager.athlete,
    student_medical_manager.id as manid,
    student_medical_manager.created_at,
    student_medical_manager.staff_notes,
    student_medical_manager.sitrep,
    student_medical_manager.sitrep_athlete,
    student_medical_manager.concussion_baseline,
    student_medical_manager.emergency_contact,
    student_medical_manager.medical_consent_agreement,
    student_medical_manager.medical_consent_agreement_status,
    student_medical_manager.physical_evaluation_1,
    student_medical_manager.physical_evaluation_2,
    student_medical_manager.cc_student_medical_history,
    student_medical_manager.cc_student_health_insurance,
    student_medical_manager.cc_student_meni_waiver,
    student_medical_manager.cc_student_immunization,
    student_medical_manager.cc_athlete_medical_history,
    student_medical_manager.cc_athlete_privacy_waiver,
    student_medical_manager.cc_athlete_reporting_waiver,
    student_medical_manager.cc_athlete_risk_waiver,
    student_medical_manager.cc_athlete_sicklecell_waiver,
    athlete_sicklecell_waiver.updated_at,
    athlete_sicklecell_waiver.results_file,
    athlete_sicklecell_waiver.results_file_status
FROM
    auth_user
LEFT JOIN
    student_profile
ON
    auth_user.id = student_profile.user_id
LEFT JOIN
    student_medical_manager
ON
    auth_user.id = student_medical_manager.user_id
AND
    student_medical_manager.created_at > "2022-06-01"
LEFT JOIN
    athlete_sicklecell_waiver
ON
    auth_user.id = athlete_sicklecell_waiver.user_id
    AND
    (
        athlete_sicklecell_waiver.proof = 1
    OR
        athlete_sicklecell_waiver.created_at > "2022-06-01"
    )
WHERE
    student_profile.class_year IN ("FN","FF","UT","PF","PN")
ORDER BY
  auth_user.last_name
