from DBconnect import conn
from DBpaper import Paper
# from DBcustomer import Customer
from sqlalchemy import create_engine, Column, BigInteger, Integer, String, SmallInteger, DECIMAL, DateTime, Enum, FLOAT
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import ForeignKey
from sqlalchemy import func
from sqlalchemy import Index

Base = declarative_base()


class Paper(Base):
    __tablename__ = 'paper'  # 数据库中的表名
    pno = Column(Integer, primary_key=True)
    pna = Column(String(45), nullable=False)
    ppr = Column(FLOAT, nullable=False)
    psi = Column(Integer, nullable=False)
    pdw = Column(String(45), nullable=False)


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


class Orders(Base):
    __tablename__ = 'orders'  # 数据库中的表名
    oid = Column(Integer, primary_key=True)
    onum = Column(Integer, nullable=False)
    pno = Column(Integer, ForeignKey('paper.pno'), nullable=False)
    gno = Column(Integer, ForeignKey('customer.gno'), nullable=False)


Base.metadata.create_all(conn.engine)


def query_all_orders():
    result = conn.query("SELECT * FROM orders")
    return result


def select_max_oid() -> int:
    with conn.session as s:
        result = s.query(func.max(Orders.oid)).scalar()
        if result:
            return result
        else:
            return 0


def select_orders_by_pno(pno):
    result = conn.query(Orders).filter(Orders.pno == pno).all()
    return result


def insert_orders(**kwargs):
    with conn.session as s:
        try:
            s.execute("select * from paper for update")
            # for name, value in kwargs.items():
            #     print(name, value)
            new_order = Orders(**kwargs)
            s.add(new_order)
            s.commit()
            return None
        except Exception as e:
            s.rollback()
            print(f"插入订单信息失败：{e}")
            return e


def select_sum_by_pno():
    with conn.session as s:
        result = s.query(Orders.pno, func.sum(Orders.onum).label('tot_num')).group_by(Orders.pno).order_by(Orders.pno.asc()).all()
        return result
