import streamlit as st


def logout():
    st.session_state['user_name'] = 'Guest'
    st.session_state["role"] = None
    st.rerun()


def gotoOrders():
    if st.button('销量查询', icon=r":material/query_stats:",
                 use_container_width=True):
        st.switch_page('pages/sales_query.py')


def gotoUser():
    if st.button('用户管理', icon=r":material/manage_accounts:", use_container_width=True):
        st.switch_page('pages/person_management.py')


def gotoPaperManagement():
    if st.button('报刊管理', icon=r":material/folder_managed:", use_container_width=True):
        st.switch_page('pages/paper_management.py')


def gotoPaperQuery():
    if st.button('报刊订阅', icon=r":material/list_alt:", use_container_width=True):
        st.switch_page('pages/paper_query.py')
