from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import BigInteger, Boolean, Column, DateTime
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method

from djtools.fields import NOW

Base = declarative_base()

class StudentMedicalManager(Base):
    __tablename__ = 'cc_student_medical_manager'

    # core
    id = Column(BigInteger, primary_key=True)
    college_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=NOW, nullable=False)
    athlete = Column(Boolean)
    sports = Column(String)
    # forms and waivers
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
