from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import BigInteger, Boolean, Column, DateTime
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method

from djtools.fields import NOW

Base = declarative_base()

class Sicklecell(Base):
    __tablename__ = 'cc_athlete_sicklecell_waiver'

    # core
    id = Column(BigInteger, primary_key=True)
    college_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=NOW, nullable=False)
    # waiver fields
    waive = Column(Boolean)
    proof = Column(Boolean)
    results = Column(String)

    def __repr__(self):
        return str(self.college_id)

