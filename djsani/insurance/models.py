from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import BigInteger, Boolean, Column, Date, DateTime
from sqlalchemy import ForeignKey, Integer, String

import datetime

"""
Reminder:

Boolean typically uses BOOLEAN or SMALLINT on the DDL side, and on
the Python side deals in ``True`` or ``False``.
"""

def _get_date():
    return datetime.datetime.now()

Base = declarative_base()

class StudentHealthInsurance(Base):
    __tablename__ = 'cc_student_health_insurance'

    # core
    id = Column(BigInteger, primary_key=True)
    college_id = Column(Integer, ForeignKey("id_rec.id"), nullable=False)
    created_at = Column(DateTime, default=_get_date, nullable=False)
    opt_out = Column(Boolean)
    # primary
    primary_policy_holder = Column(String)
    primary_dob = Column(Date)
    primary_company = Column(String)
    primary_phone = Column(String)
    primary_member_id = Column(String)
    primary_group_no = Column(String)
    primary_policy_type = Column(String)
    primary_policy_state = Column(String)
    primary_policy_address = Column(String)
    # secondary
    secondary_policy_holder = Column(String)
    secondary_dob = Column(Date)
    secondary_company = Column(String)
    secondary_phone = Column(String)
    secondary_member_id = Column(String)
    secondary_group_no = Column(String)
    secondary_policy_type = Column(String)
    secondary_policy_state = Column(String)
    secondary_policy_address = Column(String)

    def __repr__(self):
        return str(self.college_id)
