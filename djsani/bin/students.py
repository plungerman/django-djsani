# -*- coding: utf-8 -*-
import django
import os
import sys

django.setup()

# env
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djsani.settings.shell")

from django.conf import settings
from djimix.core.utils import get_connection
from djimix.core.utils import xsql
from djsani.core.sql import STUDENTS_ALPHA
from djsani.core.utils import get_term
from djtools.utils.date import calculate_age


EARL = settings.INFORMIX_ODBC


def main():
    minors = True
    term = get_term()
    cl = 'AND prog_enr_rec.cl IN ("FN","FF","FR","UT","PF","PN")'
    sql = """ {0}
        AND stu_serv_rec.yr = "{1}"
        AND stu_serv_rec.sess = "{2}"
        {3}
    """.format(
        STUDENTS_ALPHA, term['yr'], term['sess'], cl,
    )
    sql += ' ORDER BY lastname'
    with get_connection(EARL) as connection:
        # fetch the students
        cursor = connection.cursor().execute(sql)
        # obtain the column names
        columns = [column[0] for column in cursor.description]
        students = []
        for row in cursor.fetchall():
            students.append(dict(zip(columns, row)))

    minors_list = []
    for num, stu in enumerate(students):
        adult = 'minor'
        if stu.get('birth_date'):
            age = calculate_age(stu['birth_date'])
            if minors and age < settings.ADULT_AGE:
                stu['adult'] = 'minor'
                minors_list.append(stu)
            elif age >= settings.ADULT_AGE:
                adult = 'adult'
        stu['adult'] = adult

    for stu in minors_list:
        print(stu['birth_date'], stu['lastname'], stu['firstname'])


if __name__ == "__main__":
    sys.exit(main())
