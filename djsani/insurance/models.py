# -*- coding: utf-8 -*-
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import BigInteger, Boolean, Column, Date, DateTime
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.ext.hybrid import hybrid_method

import datetime
NOW = datetime.datetime.now()

Base = declarative_base()

class StudentHealthInsurance(Base):
    """
    Student health insurance data, for both students and athletes.
    """

    __tablename__ = 'cc_student_health_insurance'

    # core
    id = Column(BigInteger, primary_key=True)
    #college_id = Column(Integer, ForeignKey("id_rec.id"), nullable=False)
    college_id = Column(Integer, nullable=False)
    manager_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=NOW, nullable=False)
    opt_out = Column(Boolean)
    # primary
    primary_policy_holder = Column(String)
    primary_dob = Column(Date, default="")
    primary_company = Column(String)
    primary_phone = Column(String)
    primary_member_id = Column(String)
    primary_group_no = Column(String)
    primary_policy_type = Column(String)
    primary_policy_state = Column(String)
    primary_policy_address = Column(String)
    primary_card_front = Column(String)
    primary_card_back = Column(String)
    # secondary
    secondary_policy_holder = Column(String)
    secondary_dob = Column(Date, default="")
    secondary_company = Column(String)
    secondary_phone = Column(String)
    secondary_member_id = Column(String)
    secondary_group_no = Column(String)
    secondary_policy_type = Column(String)
    secondary_policy_state = Column(String)
    secondary_policy_address = Column(String)
    # tertiary
    tertiary_policy_holder = Column(String)
    tertiary_dob = Column(Date, default="")
    tertiary_company = Column(String)
    tertiary_phone = Column(String)
    tertiary_member_id = Column(String)
    tertiary_group_no = Column(String)
    tertiary_policy_type = Column(String)
    tertiary_policy_state = Column(String)
    tertiary_policy_address = Column(String)

    def __repr__(self):
        return str(self.college_id)

    def get_slug(self):
        return "insurance"

    def set_opt_out(self):
        """
        Method used to empty the table when a student opts out
        after previously having submitted insurance info. There
        might be a better way to do this through sqlalchemy but
        I haven't found it yet.
        """

        self.opt_out=True
        self.primary_policy_address=''
        self.primary_policy_type=''
        self.primary_policy_holder=''
        self.primary_phone=''
        self.primary_dob=''
        self.primary_group_no=''
        self.primary_member_id=''
        self.primary_company=''
        self.primary_policy_state=''
        self.secondary_company=''
        self.secondary_member_id=''
        self.secondary_group_no=''
        self.secondary_dob=''
        self.secondary_policy_state=''
        self.secondary_policy_holder=''
        self.secondary_policy_type=''
        self.secondary_policy_address=''
        self.secondary_phone=''
        self.tertiary_company=''
        self.tertiary_member_id=''
        self.tertiary_group_no=''
        self.tertiary_dob=''
        self.tertiary_policy_state=''
        self.tertiary_policy_holder=''
        self.tertiary_policy_type=''
        self.tertiary_policy_address=''
        self.tertiary_phone=''

    @hybrid_method
    def current(self, day):
        """Is this the current object for academic year?"""
        return self.created_at > day

"""
Used to empty the table when a student opts out
after previously having submitted insurance info.
There must be a better way to do this.
"""

STUDENT_HEALTH_INSURANCE = {
    'opt_out': True,
    'primary_policy_address': '',
    'primary_policy_type': '',
    'primary_policy_holder': '',
    'primary_phone': '',
    'primary_dob': '',
    'primary_group_no': '',
    'primary_member_id': '',
    'primary_company': '',
    'primary_policy_state': '',
    'secondary_company': '',
    'secondary_member_id': '',
    'secondary_group_no': '',
    'secondary_dob': '',
    'secondary_policy_state': '',
    'secondary_policy_holder': '',
    'secondary_policy_type': '',
    'secondary_policy_address': '',
    'secondary_phone': '',
    'tertiary_company': '',
    'tertiary_member_id': '',
    'tertiary_group_no': '',
    'tertiary_dob': '',
    'tertiary_policy_state': '',
    'tertiary_policy_holder': '',
    'tertiary_policy_type': '',
    'tertiary_policy_address': '',
    'tertiary_phone': '',
}
