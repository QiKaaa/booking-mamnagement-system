import streamlit as st


try:
    conn = st.connection('mysql', type='sql')
    conn.connect()
    conn_to_DB = True
    # st.success("🌞 数据库连接成功,数据写入数据库")
except Exception as e:
    st.error("💥 数据库连接失败,数据写入本地日志")
    st.error(f"错误原因：{e}")