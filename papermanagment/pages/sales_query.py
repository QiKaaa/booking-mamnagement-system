import streamlit as st
from menu import menu_with_redirect
from DBpaper import select_pna_by_pno
from DBpaper import select_ppr_by_pno
from DBorders import select_sum_by_pno
import pandas as pd

menu_with_redirect()


def calc(pno, onum) -> float:
    ppr = select_ppr_by_pno(pno)
    return ppr * onum


st.header('销量查询', divider="gray")

df = select_sum_by_pno()
df = pd.DataFrame(df)
df['tot_num'] = df['tot_num'].apply(float)
# df['ppr'] = df['pno'].apply(select_ppr_by_pno)
df['sales'] = df['pno'].apply(select_ppr_by_pno) * df['tot_num']
df['pno'] = df['pno'].map(select_pna_by_pno, na_action="ignore")


st.dataframe(
    df,
    column_config={
        'pno': st.column_config.TextColumn(
            '报刊名称',
        ),
        'tot_num': st.column_config.NumberColumn(
            '销售量',
        ),
        'sales': st.column_config.ProgressColumn(
            '销售额',
            format="¥%f",
            min_value=0,
            max_value=100,
        )
    },
    use_container_width=True,
    hide_index=True,
)
