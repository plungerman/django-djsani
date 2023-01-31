select
    count(*)
from
    cc_athlete_medical_history
where
    created_at > DATE('2022-06-01')

SELECT
    count(*)
FROM
    cc_athlete_medical_history
WHERE
    trouble_sleeping <> 'No'
AND
    created_at > DATE('2022-06-01')

SELECT
    count(*)
FROM
    cc_athlete_medical_history
WHERE
    more_energy <> 'No'
AND
    created_at > DATE('2022-06-01')

SELECT
    count(*)
FROM
    cc_athlete_medical_history
WHERE
    recurring_thoughts <> 'No'
AND
    created_at > DATE('2022-06-01')

SELECT
    count(*)
FROM
    cc_athlete_medical_history
WHERE
    anxious_nervious <> 'No'
AND
    created_at > DATE('2022-06-01')

SELECT
    count(*)
FROM
    cc_athlete_medical_history
WHERE
    depressed <> 'No'
AND
    created_at > DATE('2022-06-01')

SELECT
    count(*)
FROM
    cc_athlete_medical_history
WHERE
    lack_confidence <> 'No'
AND
    created_at > DATE('2022-06-01')

SELECT
    count(*)
FROM
    cc_athlete_medical_history
WHERE
    despair <> 'No'
AND
    created_at > DATE('2022-06-01')

SELECT
    count(*)
FROM
    cc_athlete_medical_history
WHERE
    lack_emotional_control <> 'No'
AND
    created_at > DATE('2022-06-01')

SELECT
    count(*)
FROM
    cc_athlete_medical_history
WHERE
    self_others_harm <> 'No'
AND
    created_at > DATE('2022-06-01')
