SELECT
    id_rec.lastname, id_rec.firstname,
    cvid_rec.ldap_name,
    id_rec.id,
    cc_student_medical_history.allergies_medical,
cc_student_medical_history.allergies_other,
         cc_student_medical_history.anemia,
                  cc_student_medical_history.anxiety,
                 cc_student_medical_history.bronchospasm,
            cc_student_medical_history.adhd_add,
                cc_student_medical_history.birth_defect,
            cc_student_medical_history.blood_disorder,
          cc_student_medical_history.bronchitis,
cc_student_medical_history.cancer,
cc_student_medical_history.chicken_pox,
cc_student_medical_history.counseling,
              cc_student_medical_history.depression,
              cc_student_medical_history.diabetes,
                cc_student_medical_history.eating_disorder,
         cc_student_medical_history.ent_disorder,
            cc_student_medical_history.headaches,
               cc_student_medical_history.head_injury,
             cc_student_medical_history.heart_condition,
         cc_student_medical_history.hepatitis,
               cc_student_medical_history.hernia,
                  cc_student_medical_history.hyper_tension,
           cc_student_medical_history.hiv_aids,
                cc_student_medical_history.hospitalizations,
        cc_student_medical_history.ibd,
                     cc_student_medical_history.kidney_urinary,
cc_student_medical_history.medications,
             cc_student_medical_history.meningitis,
              cc_student_medical_history.mononucleosis,
           cc_student_medical_history.mrsa,
                    cc_student_medical_history.organ_loss,
              cc_student_medical_history.pneumonia,
               cc_student_medical_history.rheumatic_fever,
         cc_student_medical_history.seizure_disorder,
        cc_student_medical_history.stroke,
                  cc_student_medical_history.substance_abuse,
         cc_student_medical_history.thyroid_disorder,
        cc_student_medical_history.tuberculosis,
            cc_student_medical_history.other_condition
FROM
    id_rec
LEFT JOIN
    cvid_rec     ON  id_rec.id = cvid_rec.cx_id
LEFT JOIN
    cc_student_medical_history ON  id_rec.id = cc_student_medical_history.college_id
LEFT JOIN
    cc_student_medical_manager ON  id_rec.id = cc_student_medical_manager.college_id
WHERE
    cc_student_medical_manager.cc_student_medical_history = 1
ORDER BY
    id_rec.lastname
