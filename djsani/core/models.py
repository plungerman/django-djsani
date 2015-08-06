# -*- coding: utf-8 -*-
from django.utils.encoding import smart_text

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import BigInteger, SmallInteger, Boolean, Column, DateTime, Text
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method

import datetime
NOW = datetime.datetime.now()

ADDITION = 1
CHANGE = 2
DELETION = 3

Base = declarative_base()

class StudentMedicalContentType(Base):
    __tablename__ = 'cc_student_medical_content_type'

    id = Column(BigInteger, primary_key=True)
    name = Column(String)
    app_label = Column(String)
    model = Column(String)

    def __repr__(self):
        return self.model

class StudentMedicalLogEntry(Base):
    __tablename__ = 'cc_student_medical_log_entry'

    id = Column(BigInteger, primary_key=True)
    college_id = Column(Integer, nullable=False)
    action_time = Column(DateTime, default=NOW, nullable=False)
    content_type_id = Column(Integer)
    object_id = Column(Integer)
    object_repr = Column(String)
    action_flag = Column(SmallInteger)
    action_message = Column(Text)

    def __repr__(self):
        return smart_text(self.action_time)

    def __str__(self):
        if self.action_flag == ADDITION:
            return ('Added "%(object)s".') % {'object': self.object_repr}
        elif self.action_flag == CHANGE:
            return ('Changed "%(object)s" - %(changes)s') % {
                'object': self.object_repr,
                'changes': self.change_message,
            }
        elif self.action_flag == DELETION:
            return ('Deleted "%(object)s."') % {'object': self.object_repr}

        return ugettext('LogEntry Object')

    def is_addition(self):
        return self.action_flag == ADDITION

    def is_change(self):
        return self.action_flag == CHANGE

    def is_deletion(self):
        return self.action_flag == DELETION


class StudentMedicalManager(Base):
    __tablename__ = 'cc_student_medical_manager'

    # core
    id = Column(BigInteger, primary_key=True)
    college_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=NOW, nullable=False)
    sitrep = Column(Boolean)
    athlete = Column(Boolean)
    sports = Column(String)
    emergency_contact = Column(Boolean)
    # forms and waivers
    cc_student_immunization = Column(Boolean)
    cc_student_medical_history = Column(Boolean)
    cc_student_health_insurance = Column(Boolean)
    cc_student_meni_waiver = Column(Boolean)
    cc_athlete_medical_history = Column(Boolean)
    cc_athlete_privacy_waiver = Column(Boolean)
    cc_athlete_reporting_waiver = Column(Boolean)
    cc_athlete_risk_waiver = Column(Boolean)
    cc_athlete_sicklecell_waiver = Column(Boolean)

    def __repr__(self):
        return str(self.college_id)

    #@hybrid_property
    @hybrid_method
    def current(self, day):
        """Is this the current manager for academic year?"""
        return self.created_at > day
    #current = property(_get_current)

# IDs must be unique pattern that does not repeat in any other
# item e.g 25 & 250 will not work.
SPORTS_MEN = (
    ("0","----Men's Sport----"),
    ("15","Baseball"),
    ("25","Basketball"),
    ("35","Cross Country"),
    ("45","Football"),
    ("55","Golf"),
    ("60","Ice Hockey"),
    ("65","Lacrosse"),
    ("75","Soccer"),
    ("85","Swimming"),
    ("95","Tennis"),
    ("105","Track &amp; Field"),
    ("120","Volleyball"),
)
SPORTS_WOMEN = (
    ("0","----Women's Sports----"),
    ("200","Basketball"),
    ("210","Cross Country"),
    ("220","Golf"),
    ("225","Ice Hockey"),
    ("230","Lacrosse"),
    ("240","Soccer"),
    ("260","Softball"),
    ("270","Swimming"),
    ("280","Tennis"),
    ("290","Track &amp; Field"),
    ("300","Volleyball"),
    ("305","Water Polo")
)

SPORTS = SPORTS_WOMEN + SPORTS_MEN
