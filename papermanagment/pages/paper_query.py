import streamlit as st
import pandas as pd
import time
from menu import menu_with_redirect
from streamlit_modal import Modal
import DBpaper
import DBorders
import DBcustomer
import copy

# Redirect to app.py if not logged in, otherwise show the navigation menu
menu_with_redirect()

df_key = 'paper_key'
df_selected_key = 'paper_selected_key'
df = DBpaper.query_all_paper()
if df_key not in st.session_state:
    st.session_state[df_key] = df

df = pd.DataFrame(df)
copy_df = copy.deepcopy(st.session_state[df_key])
st.session_state['gna'] = None
st.session_state['gte'] = None
st.session_state['gad'] = None
st.session_state['gpo'] = None
st.session_state['order'] = None
st.session_state['tot_price'] = None

column_configuration_dataframe = {
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
}

column_configuration_data_editor = {
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
}

st.header("报刊订阅")
# st.text("\n")
select, ask_num, profile = st.tabs(["选择订购报刊", "填写订阅份数", "填写个人信息"])
with select:
    paper_query = st.dataframe(
        copy_df,
        column_config=column_configuration_dataframe,
        use_container_width=True,
        hide_index=True,
        on_select="rerun",
        selection_mode="multi-row",
    )

with ask_num:
    paper_selected = paper_query.selection.rows
    df_selected = copy_df.iloc[paper_selected]
    df_selected['onum'] = None
    paper_selected = st.data_editor(
        df_selected,
        column_config=column_configuration_data_editor,
        hide_index=True,
        use_container_width=True,
        disabled=("pno", "pno", "ppr", "psi", "pdw"),
        key=df_selected_key
    )

with profile:
    st.session_state['gna'] = st.text_input('姓名')
    st.session_state['gte'] = st.text_input('联系方式', max_chars=11)
    st.session_state['gad'] = st.text_input('地址')
    st.session_state['gpo'] = st.text_input('邮政编码')


def is_legal_order():
    if 'gna' not in st.session_state or st.session_state['gna'] is None or st.session_state['gna'].strip() == '':
        st.error('请填写您的姓名')
        return False
    if 'gte' not in st.session_state or st.session_state['gte'] is None or st.session_state['gte'].strip() == '':
        st.error('请填写您的联系方式')
        return False
    if 'gad' not in st.session_state or st.session_state['gad'] is None or st.session_state['gad'].strip() == '':
        st.error('请填写您的联系地址')
        return False
    if 'gpo' not in st.session_state or st.session_state['gpo'] is None or st.session_state['gpo'].strip() == '':
        st.error('请填写您的邮政编码')
        return False
    if st.session_state['gte'].isdigit() == False or len(st.session_state['gte']) != 11:
        st.error('请检查您的联系方式')
        return False
    if st.session_state['gpo'].isdigit() == False or len(st.session_state['gpo']) != 6:
        st.error('请检查您的邮政编码')
        return False
    if df_selected is None:
        st.error('请选择订阅报刊')
        return False
    edited_rows = st.session_state[df_selected_key].get('edited_rows')
    if edited_rows is None:
        st.error('请填写报刊订阅信息')
        return False
    return True


@st.dialog("请确认您的订单")
def order_confirm():
    sum = 0.0
    edited_rows = st.session_state[df_selected_key].get('edited_rows')
    print(df_selected)
    print(edited_rows)

    for idx, row in edited_rows.items():
        pno = df_selected.loc[df_selected.index[idx], 'pno']
        ppr = DBpaper.select_ppr_by_pno(pno)
        for name, value in row.items():
            if name == 'onum':
                sum = sum + ppr * value * 1.0

    st.text(f"亲爱的{st.session_state['gna']}，您订阅的报刊共计 {sum} 元")
    st.text("以下是您的订单")
    st.dataframe(paper_selected)

    if st.button('确认订单'):
        st.session_state['tot_price'] = sum
        st.session_state['order'] = paper_selected
        nw_gno = DBcustomer.select_customer_by_gna_gte(st.session_state['gna'], st.session_state['gte'])
        if nw_gno is None:
            nw_gno = DBcustomer.select_max_gno() + 1
            DBcustomer.insert_customer(
                gno=nw_gno,
                gna=st.session_state['gna'],
                gte=st.session_state['gte'],
                gad=st.session_state['gad'],
                gpo=st.session_state['gpo'],
            )

        nw_oid = DBorders.select_max_oid() + 1
        for idx, row in edited_rows.items():
            nw_pno = df_selected.loc[df_selected.index[idx], 'pno']
            nw_onum=0
            for name, value in row.items():
                if name=='onum':
                    nw_onum=value
                    break
            DBorders.insert_orders(
                oid=nw_oid,
                onum=nw_onum,
                pno=nw_pno,
                gno=nw_gno,
            )
            nw_oid = nw_oid + 1
        st.success("提交成功，三秒后为您开具发票...")
        time.sleep(2)
        st.switch_page("pages/receipt.py")


if st.button("提交订单"):
    # order_confirm()
    if is_legal_order():
        print("legal!")
        order_confirm()
