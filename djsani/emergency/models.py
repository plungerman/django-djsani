from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime
from sqlalchemy import Integer, String

Base = declarative_base()

class AARec(Base):
    __tablename__ = 'aa_rec'

    # core
    id = Column(Integer)
    aa = Column(String)
    beg_date = Column(DateTime)
    end_date = Column(DateTime)
    # contact info
    peren = Column(String)
    line1 = Column(String)
    line2 = Column(String)
    line3 = Column(String)
    city = Column(String)
    st = Column(String)
    zip = Column(String)
    ctry = Column(String)
    phone = Column(String)
    phone_ext = Column(String)
    ofc_add_by = Column(String)
    cass_cert_date = Column(DateTime)
    aa_no = Column(Integer, primary_key=True)
    cell_carrier = Column(String)
    opt_out = Column(String)

    def __repr__(self):
        return str(self.id)
