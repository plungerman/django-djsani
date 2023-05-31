# -*- coding: utf-8 -*-

from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from djtools.utils.users import in_group


def eligibility(view_func):
    """Check the user for eligibility to access the forms."""
    def _wrap(request, *args, **kwargs):
        """Wrapper for the decorator."""
        staff = in_group(request.user, settings.STAFF_GROUP)
        coach = in_group(request.user, settings.COACH_GROUP)
        if coach:
            staff = True
        user = request.user
        try:
            student = user.student
        except Exception:
            student = None
        if settings.ACADEMIC_YEAR_LIMBO and not staff:
            return render(request, 'closed.html')
        elif student and student.birth_date and student.gender and student.residency and student.class_year:
            return view_func(request, *args, **kwargs)
        else:
            response = render(request, 'missing.html')
            if staff:
                response = HttpResponseRedirect(reverse_lazy('dashboard_home'))
            return response
    return _wrap
