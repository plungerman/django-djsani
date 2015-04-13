from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import BigInteger, Boolean, Column, DateTime
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.ext.hybrid import hybrid_method

import datetime
NOW = datetime.datetime.now()

Base = declarative_base()

class Sicklecell(Base):
    __tablename__ = 'cc_athlete_sicklecell_waiver'

    # core
    id = Column(BigInteger, primary_key=True)
    college_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=NOW, nullable=False)
    updated_at = Column(DateTime, default=NOW, nullable=False)
    # waiver fields
    waive = Column(Boolean)
    proof = Column(Boolean)
    results = Column(String)

    def __repr__(self):
        return str(self.college_id)


class Meni(Base):
    __tablename__ = 'cc_student_meni_waiver'

    # core
    id = Column(BigInteger, primary_key=True)
    college_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=NOW, nullable=False)
    # waiver fields
    agree = Column(Boolean)

    def __repr__(self):
        return str(self.college_id)

    @hybrid_method
    def current(self, day):
        """Is this the current waiver for academic year?"""
        return self.created_at > day


class Risk(Base):
    __tablename__ = 'cc_athlete_risk_waiver'

    # core
    id = Column(BigInteger, primary_key=True)
    college_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=NOW, nullable=False)
    # waiver fields
    agree = Column(Boolean)

    def __repr__(self):
        return str(self.college_id)

    @hybrid_method
    def current(self, day):
        """Is this the current waiver for academic year?"""
        return self.created_at > day


class Reporting(Base):
    __tablename__ = 'cc_athlete_reporting_waiver'

    # core
    id = Column(BigInteger, primary_key=True)
    college_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=NOW, nullable=False)
    # waiver fields
    agree = Column(Boolean)

    def __repr__(self):
        return str(self.college_id)

    @hybrid_method
    def current(self, day):
        """Is this the current waiver for academic year?"""
        return self.created_at > day


class Privacy(Base):
    __tablename__ = 'cc_athlete_privacy_waiver'
    # core
    id = Column(BigInteger, primary_key=True)
    college_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=NOW, nullable=False)
    # waiver fields
    ncaa_tool = Column(Boolean)
    medical_insurance = Column(Boolean)
    news_media = Column(Boolean) # required False
    parents_guardians = Column(Boolean)
    disclose_records = Column(Boolean)

    def __repr__(self):
        return str(self.college_id)

    @hybrid_method
    def current(self, day):
        """Is this the current waiver for academic year?"""
        return self.created_at > day


