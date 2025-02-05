import streamlit as st


def authenticated_menu():
    # Show a navigation menu for authenticated users
    st.sidebar.page_link("app.py", label="导航", icon=r":material/home:")

    st.sidebar.page_link("pages/paper_query.py", label="报刊订阅", icon=r":material/list_alt:")
    if st.session_state.role in ["admin", "super_admin"]:
        st.sidebar.page_link("pages/paper_management.py", label="报刊管理", icon=r":material/folder_managed:")

    st.sidebar.page_link("pages/sales_query.py", label="销量查询", icon=r":material/query_stats:")

    if st.session_state.role in ["super_admin"]:
        st.sidebar.page_link("pages/person_management.py", label="用户管理", icon=r":material/manage_accounts:")

    st.sidebar.page_link("pages/logout.py", label="登出", icon=r":material/logout:")


def unauthenticated_menu():
    # Show a navigation menu for unauthenticated users
    st.sidebar.page_link("app.py", label="登录", icon=r":material/login:")


def menu():
    # Determine if a user is logged in or not, then show the correct
    # navigation menu
    if "role" not in st.session_state or st.session_state.role is None:
        unauthenticated_menu()
        return
    authenticated_menu()


def menu_with_redirect():
    # Redirect users to the main page if not logged in, otherwise continue to
    # render the navigation menu
    if "role" not in st.session_state or st.session_state.role is None:
        st.switch_page("app.py")
    menu()
