import streamlit as st
from DBconnect import conn
from sqlalchemy import create_engine, Column, BigInteger, Integer, String, SmallInteger, DECIMAL, DateTime, Enum
from sqlalchemy.orm import declarative_base, sessionmaker


Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'  # 数据库中的表名
    uid = Column(String(45), primary_key=True)
    password = Column(String(45), nullable=False)
    admin = Column(Enum('0', '1', '2'), nullable=False)

    def __repr__(self):
        return f"<Users(uid={self.uid}, password={self.password}, auth={self.admin}, "


Base.metadata.create_all(conn.engine)


def auth_users(uid: str = None, password: str = None) -> int:
    ret = -1
    if uid is not None and password is not None:
        with conn.session as s:
            result = s.query(Users).filter(Users.uid == uid).one()
            if result.password == password:
                ret = result.admin
            else:
                ret = -1
            s.commit()
    return int(ret)


def select_users():
    result = None
    sql = "select * from users"
    result = conn.query(sql)
    return result


def delete_users(uid: int) -> bool:
    with conn.session as s:
        try:
            s.execute("select * from users for update")
            result = s.query(Users).filter(Users.uid == uid)
            result.delete()
            s.commit()
            return True
        except:
            s.rollback()
            return False


def update_users(uid: int, password: str = None, admin: str = None) -> bool:
    with conn.session as s:
        try:
            s.execute("select * from users for update")
            user = s.query(Users).filter(Users.uid == uid).first()
            if user:
                if password is not None:
                    user.password = password
                if admin is not None:
                    user.admin = admin
            s.commit()
            return True
        except:
            s.rollback()
            return False


def insert_users(uid: int, password: str, admin: str):
    with conn.session as s:
        try:
            new_user = Users(uid=uid, password=password, admin=admin)
            s.add(new_user)
            s.commit()
            return None
        except Exception as e:
            s.rollback()
            raise e