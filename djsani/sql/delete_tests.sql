select * from cc_student_medical_manager where created_at > DATE('2017-05-01');
delete from cc_student_medical_manager where created_at > DATE('2017-05-01');

select * from cc_student_health_insurance where created_at > DATE('2017-05-01')
delete from cc_student_health_insurance where created_at > DATE('2017-05-01');

select * from cc_student_medical_history where created_at > DATE('2017-05-01');
delete from cc_student_medical_history where created_at > DATE('2017-05-01');

select * from cc_student_meni_waiver where created_at > DATE('2017-05-01');
None

select * from cc_athlete_medical_history where created_at > DATE('2017-05-01');
delete  from cc_athlete_medical_history where created_at > DATE('2017-05-01');

select * from cc_athlete_privacy_waiver where created_at > DATE('2017-05-01');
None

select * from cc_athlete_reporting_waiver where created_at > DATE('2017-05-01');
None

select * from cc_athlete_risk_waiver where created_at > DATE('2017-05-01');
None

select * from cc_athlete_sicklecell_waiver where created_at > DATE('2017-05-01');
None
