from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import BigInteger, Boolean, Column, Date, DateTime
from sqlalchemy import ForeignKey, Integer, String

import datetime

def _get_date():
    return datetime.datetime.now()

Base = declarative_base()

class StudentMedicalManager(Base):
    __tablename__ = 'cc_student_medical_manager'

    # core
    id = Column(BigInteger, primary_key=True)
    college_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=_get_date, nullable=False)
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
