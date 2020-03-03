# -*- coding: utf-8 -*-

"""Data models."""

from django.db import models


class AARec(models.Model):
    """aa_rec table for contact information."""

    # core
    id = models.IntegerField()
    aa = models.CharField(max_length=4)
    beg_date = models.DateField()
    end_date = models.DateField()
    # contact info
    peren = models.CharField(max_length=1)
    line1 = models.CharField(max_length=64)
    line2 = models.CharField(max_length=64)
    line3 = models.CharField(max_length=64)
    city = models.CharField(max_length=50)
    st = models.CharField(max_length=2)
    zip = models.CharField(max_length=10)
    ctry = models.CharField(max_length=3)
    phone = models.CharField(max_length=12)
    phone_ext = models.CharField(max_length=4)
    ofc_add_by = models.CharField(max_length=4)
    cass_cert_date = models.DateField()
    aa_no = models.AutoField(primary_key=True)
    cell_carrier = models.CharField(max_length=4)
    opt_out = models.CharField(max_length=1)

    class Meta:
        """Attributes about the data model and admin options."""

        db_table = 'aa_rec'

    def __repr__(self):
        """Default data for display."""
        return str(self.id)
