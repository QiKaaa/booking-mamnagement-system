from enum import Enum


class AuthLevel(Enum):
    user = 0
    admin = 1
    super_admin = 2


class AuthName(Enum):
    user = "用户"
    admin = "管理员"
    super_admin = "超级管理员"


pno = 5


def get_pno():
    global pno
    pno = (pno + 1)%1000000
    return pno