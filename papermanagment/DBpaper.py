from DBconnect import conn
from sqlalchemy import create_engine, Column, BigInteger, Integer, String, SmallInteger, DECIMAL, DateTime, Enum, FLOAT
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


class Paper(Base):
    __tablename__ = 'paper'  # 数据库中的表名
    pno = Column(Integer, primary_key=True)
    pna = Column(String(45), nullable=False)
    ppr = Column(FLOAT, nullable=False)
    psi = Column(Integer, nullable=False)
    pdw = Column(String(45), nullable=False)


Base.metadata.create_all(conn.engine)


def query_all_paper():
    result = conn.query("SELECT * FROM PAPER")
    return result


def select_pna_by_pno(pno):
    with conn.session as s:
        result=s.query(Paper).filter(Paper.pno == pno).first()
        if result:
            return result.pna
        else:
            return None
def select_ppr_by_pno(pno) -> float:
    with conn.session as s:
        result = s.query(Paper).filter(Paper.pno == pno).first()
        if result:
            return result.ppr
        else:
            return 0.0


def insert_paper(**kwargs):
    with conn.session as s:
        try:
            s.execute("select * from paper for update")
            for name, value in kwargs.items():
                print(name, value)
            new_paper = Paper(**kwargs)
            s.add(new_paper)
            s.commit()
            return None
        except Exception as e:
            s.rollback()
            print(f"插入报纸信息失败：{e}")
            return e


def update_paper(pno, **kwargs):
    with conn.session as s:
        try:
            s.execute("select * from paper for update")
            paper = s.query(Paper).filter(Paper.pno == pno).first()
            if paper:
                for name, value in kwargs.items():
                    paper.__setattr__(name, value)
            s.commit()
            return None
        except Exception as e:
            s.rollback()
            return e


def delete_paper(pno: int):
    with conn.session as s:
        try:
            s.execute("select * from paper for update")
            result = s.query(Paper).filter(Paper.pno == pno)
            result.delete()
            s.commit()
        except Exception as e:
            s.rollback()
            print(f"删除报纸信息失败：{e}")
            raise e
