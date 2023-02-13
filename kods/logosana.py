from sqlalchemy.orm import sessionmaker, Session

from kods.models import Auditacija as Aa
from sqlalchemy import create_engine, DateTime
import datetime
from config import DATABASE_URI


engine = create_engine(DATABASE_URI)


def logi(logs):
    print(logs)


# def auditacija(darbiba: str = '', laiks: DateTime = datetime.datetime.utcnow, parametri: str = '',
#                autorizacijas_lvl: str = '', statuss: str = ''):
#     try:
#         audit = Aa()
#         audit.darbiba = darbiba
#         #audit.laiks = laiks
#         audit.parametri = parametri
#         audit.autorizacijas_lvl = autorizacijas_lvl
#         audit.statuss = statuss
#
#         try:
#             #Base.metadata.create_all(engine)
#             session = sessionmaker(bind=engine)
#             s = session()
#
#             s.add(audit)
#             s.commit()
#         except Exception as e:
#             logi("Kļūda darbojoties ar db: " + str(e))
#         finally:
#             s.close()
#     except Exception as e:
#         logi("Kļūda piešķirot auditācijas vērtības: " + str(e))


def auditacijas(darbiba: str = '', laiks: DateTime = datetime.datetime.utcnow, parametri: str = '',
               autorizacijas_lvl: str = '', statuss: str = '', metrika: int = 0):
    try:
        audit = Aa()
        audit.darbiba = darbiba
        #audit.laiks = laiks
        audit.parametri = parametri
        audit.autorizacijas_lvl = autorizacijas_lvl
        audit.statuss = statuss
        audit.metrika = metrika

        try:
            with Session(engine) as s:
                s.add(audit)
                s.commit()
        except Exception as e:
            logi("Kļūda darbojoties ar db: " + str(e))
    except Exception as e:
        logi("Kļūda piešķirot auditācijas vērtības: " + str(e))