import streamlit as st
from menu import menu_with_redirect

# menu_with_redirect()


st.header("发票开具")

container = st.container(border=True)
container.text(f"购买人：{st.session_state['gna']}")
container.dataframe(
    st.session_state['order'],
    column_config={
    'pno': st.column_config.NumberColumn(
        label='报纸编号',
        min_value=0,
        max_value=999999,
        default=0,
        format="%06d",
        required=True,
    ),
    'pna': st.column_config.TextColumn(
        label='报纸名称',
        required=True,
    ),
    'ppr': st.column_config.NumberColumn(
        label='单价',
        min_value=0.0,
        format="¥%f",
        required=True,
    ),
    'psi': st.column_config.NumberColumn(
        label=' 版面',
        min_value=0,
        required=True,
    ),
    'pdw': st.column_config.TextColumn(
        label='出版单位',
        required=True,
    ),
    'onum': st.column_config.NumberColumn(
        label='订购数量',
        default=None,
        min_value=1,
        max_value=99
    )
    },
    hide_index=True,
    use_container_width=True
)
container.text(f"合计：¥{st.session_state['tot_price']}")

if st.button("返回主页"):
    st.session_state['gna'] = None
    st.session_state['gte'] = None
    st.session_state['gad'] = None
    st.session_state['gpo'] = None
    st.session_state['order'] = None
    st.session_state['tot_price'] = None
    st.switch_page('./app.py')
