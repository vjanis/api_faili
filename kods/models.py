from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, DateTime, Sequence

import datetime


class Base(DeclarativeBase):
    pass


class Auditacija(Base):
    __tablename__ = 'auditacija'
    id = Column(Integer, Sequence('auditacija_id_seq'), primary_key=True)
    laiks = Column(DateTime, default=datetime.datetime.utcnow)
    darbiba = Column(String)
    parametri = Column(String)
    json_text = Column(JSONB)
    autorizacijas_lvl = Column(String)
    statuss = Column(String)
    metrika = Column(Integer)

    def __repr__(self):
        return "<Auditacija(id='{}', laiks='{}', darbiba={}, parametri={}, json_text={}, " \
               "autorizacijas_lvl={}, statuss={}, metrika={})>" \
            .format(self.id, self.laiks, self.darbiba, self.parametri, self.json_text,
                    self.autorizacijas_lvl, self.statuss, self.metrika)
