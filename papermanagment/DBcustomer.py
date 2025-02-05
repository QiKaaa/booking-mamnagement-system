from DBconnect import conn
from sqlalchemy import create_engine, Column, BigInteger, Integer, String, SmallInteger, DECIMAL, DateTime, Enum, FLOAT
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Index
from sqlalchemy import func

Base = declarative_base()


class Customer(Base):
    __tablename__ = 'customer'  # 数据库中的表名
    gno = Column(Integer, primary_key=True)
    gna = Column(String(45), nullable=False)
    gte = Column(String(45), nullable=False)
    gad = Column(String(100), nullable=False)
    gpo = Column(String(45), nullable=False)
    __table_args__ = (
        Index('gna_gte', "gna", "gte"),
    )


Base.metadata.create_all(conn.engine)


def select_max_gno()->int:
    with conn.session as s:
        result = s.query(func.max(Customer.gno)).scalar()
        if result:
            return result
        else:
            return 0.0


def select_customer_by_gna_gte(gna, gte):
    with conn.session as s:
        result = s.query(Customer).filter(Customer.gna == gna and Customer.gte == gte).first()
        if result:
            return result.gno
        else:
            return None


def insert_customer(**kwargs):
    with conn.session as s:
        try:
            s.execute("select * from paper for update")
            for name, value in kwargs.items():
                print(name, value)
            new_customer = Customer(**kwargs)
            s.add(new_customer)
            s.commit()
            return None
        except Exception as e:
            s.rollback()
            print(f"插入报纸信息失败：{e}")
            return e
