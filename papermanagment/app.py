import streamlit as st
from menu import menu
from DBusers import auth_users
from config import AuthLevel
from config import AuthName
from DBconnect import conn_to_DB
import ButtonOp

# Initialize st.session_state.role to None
if 'role' not in st.session_state:
    st.session_state['role'] = None

if 'user_name' not in st.session_state:
    st.session_state['user_name'] = 'Guest'


def GuideButton_user():
    left, right = st.columns(2, gap="medium")
    with left:
        ButtonOp.gotoPaperQuery()
        # st.button('查询报刊', icon=r":material/plagiarism:", use_container_width=True)
    with right:
        ButtonOp.gotoOrders()
        # st.button('查询订单', icon=r":material/query_stats:",
        #           use_container_width=True)


def GuideButton_admin():
    left, middle, right = st.columns(3, gap="medium")
    with left:
        ButtonOp.gotoPaperQuery()
        # st.button('查询报刊', icon=r":material/plagiarism:", use_container_width=True)
    with middle:
        ButtonOp.gotoPaperManagement()
        # st.button('查询订单', icon=r":material/query_stats:",
        #           use_container_width=True)
    with right:
        ButtonOp.gotoOrders()
        # st.button('用户管理', icon=r":material/manage_accounts:", use_container_width=True)


def GuideButton_superadmin():
    left, m1, m2, right = st.columns(4, gap="medium")
    with left:
        ButtonOp.gotoPaperQuery()
    with m1:
        ButtonOp.gotoPaperManagement()
    with m2:
        ButtonOp.gotoUser()
    with right:
        ButtonOp.gotoOrders()


def login_process():
    if 'role' not in st.session_state or st.session_state["role"] is None:
        user = st.text_input("用户名")
        password = st.text_input("密码", type="password")
        if conn_to_DB is False:
            st.error("无法登录，请联系管理员维修")
            return
        if st.button('登录'):
            role = auth_users(user, password)
            if role != -1:
                role = AuthLevel(role).name
                st.session_state["user_name"] = user
                st.session_state["role"] = role
                st.rerun()
            else:
                st.error('登陆失败，请检查用户名和密码')
    else:
        # st.write(f"##  👋欢迎登录邮局报刊订阅系统，{st.session_state["user_name"]}")
        st.success(f"登陆成功，您的身份是 {AuthName[st.session_state["role"]].value}")
        if st.session_state["role"] is 'user':
            GuideButton_user()
        else:
            if st.session_state["role"] is 'admin':
                GuideButton_admin()
            else:
                GuideButton_superadmin()


st.header("邮局订报管理系统")
login_process()
menu()  # Render the dynamic menu!
