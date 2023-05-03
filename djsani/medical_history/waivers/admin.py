# -*- coding: utf-8 -*-

from django.contrib import admin
from djsani.medical_history.waivers.models import Meni
from djsani.medical_history.waivers.models import Privacy
from djsani.medical_history.waivers.models import Risk
from djsani.medical_history.waivers.models import Reporting
from djsani.medical_history.waivers.models import Sicklecell


class WaiverAdmin(admin.ModelAdmin):
    """Generice admin class for athlete medical waiver."""

    raw_id_fields = ('user', 'manager')


admin.site.register(Meni, WaiverAdmin)
admin.site.register(Privacy, WaiverAdmin)
admin.site.register(Risk, WaiverAdmin)
admin.site.register(Reporting, WaiverAdmin)
admin.site.register(Sicklecell, WaiverAdmin)
