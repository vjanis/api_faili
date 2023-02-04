from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime

import datetime

Base = declarative_base()


class Auditacija(Base):
    __tablename__ = 'auditacija'
    id = Column(Integer, primary_key=True)
    laiks = Column(DateTime, default=datetime.datetime.utcnow)
    darbiba = Column(String)
    parametri = Column(String)
    autorizacijas_lvl = Column(String)
    statuss = Column(String)

    def __repr__(self):
        return "<Auditacija(id='{}', laiks='{}', darbiba={}, parametri={}, autorizacijas_lvl={}, statuss={})>" \
            .format(self.id, self.laiks, self.darbiba, self.parametri, self.autorizacijas_lvl, self.statuss)
