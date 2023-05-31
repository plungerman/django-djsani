# -*- coding: utf-8 -*-

from django.conf import settings


# e.g. 2015-05-01 00:00:00
START_DATE = settings.START_DATE
STUDENTS_ALPHA = """
SELECT
    DISTINCT
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
    student_health_insurance.opt_out,
    student_health_insurance.primary_policy_type,
    student_health_insurance.tertiary_company,
    athlete_sicklecell_waiver.updated_at,
    athlete_sicklecell_waiver.results_file,
    athlete_sicklecell_waiver.results_file_status
FROM
    student_profile
LEFT JOIN
    auth_user
ON
    student_profile.user_id = auth_user.id
LEFT JOIN
    student_medical_manager
ON
    student_profile.user_id = student_medical_manager.user_id
AND
    student_medical_manager.created_at > "{0}"
LEFT JOIN
    student_health_insurance
ON
    student_medical_manager.id = student_health_insurance.manager_id
AND
    student_health_insurance.created_at > "{1}"
LEFT JOIN
    athlete_sicklecell_waiver
ON
    student_profile.user_id = athlete_sicklecell_waiver.user_id
    AND
    (
        athlete_sicklecell_waiver.proof = 1
    OR
        athlete_sicklecell_waiver.created_at > "{2}"
    )
WHERE
    student_profile.status = 1
""".format(START_DATE, START_DATE, START_DATE)
