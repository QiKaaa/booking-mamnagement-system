import streamlit as st
import pandas as pd
from menu import menu_with_redirect
from get_editor_key import get_editor_key
import DBpaper

# Redirect to app.py if not logged in, otherwise show the navigation menu
menu_with_redirect()

st.header("报刊管理", divider="gray")
st.markdown("✅ 你可以在此页实现对报刊信息的添加、删除和对报刊信息的修改")
st.markdown("✅ 点击下方空白行添加新报刊")
st.markdown("✅ 直接点击要修改的单元格对已有报刊的信息进行修改")

df_key = 'paper_key'
df_editor_key = get_editor_key(df_key)
df = DBpaper.query_all_paper()
df = pd.DataFrame(df)
# print(df_key)
if df_key not in st.session_state:
    st.session_state[df_key] = df

paper_editor = st.data_editor(
    st.session_state[df_key],
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
            required = True,
        ),
    },
    use_container_width=True,
    num_rows="dynamic",
    disabled=False,
    key=df_editor_key,
    hide_index=True,
)


def data_editor_change(key, editor_key):
    """Callback function of data_editor. """
    st.session_state[key] = apply_de_change(st.session_state[key], st.session_state[editor_key])


def apply_de_change(df0, changes):
    """Apply changes of data_editor."""
    add_rows = changes.get('added_rows')
    edited_rows = changes.get('edited_rows')
    deleted_rows = changes.get('deleted_rows')

    for idx, row in edited_rows.items():
        pno = df.loc[df.index[idx], 'pno']
        for name, value in row.items():
            df0.loc[df0.index[idx], name] = value
        e = DBpaper.update_paper(pno, **row)
        if e is not None:
            st.error(e)
            print(e)

    for idx in deleted_rows:
        pno = df.loc[df.index[idx], 'pno']
        DBpaper.delete_paper(pno)
    df0.drop(df0.index[deleted_rows], inplace=True)

    ss = []
    has_index = add_rows and '_index' in add_rows[0]
    for add_row in add_rows:
        print(add_row)
        e = DBpaper.insert_paper(**add_row)
        if e is not None:
            st.error(e)
            print(e)
        if '_index' in add_row:
            ss.append(pd.Series(data=add_row, name=add_row.pop('_index')))
        else:
            ss.append(pd.Series(data=add_row))

    df_add = pd.DataFrame(ss)

    return pd.concat([df0, df_add], axis=0) if has_index else pd.concat([df0, df_add], axis=0, ignore_index=True)


if st.button("提交修改"):
    data_editor_change(df_key, df_editor_key)
    st.success("报刊信息修改成功")
