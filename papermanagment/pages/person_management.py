import streamlit as st
import pandas as pd
import hashlib
import DBusers
from menu import menu_with_redirect
from get_editor_key import get_editor_key

# Redirect to app.py if not logged in, otherwise show the navigation menu
menu_with_redirect()

# Verify the user's role
if st.session_state.role not in ["admin", "super_admin"]:
    st.warning("You do not have permission to view this page.")
    st.stop()

st.header("用户管理", divider="gray")
st.markdown("✅ 你可以在此页实现对用户的添加、删除和对用户信息的修改")
st.markdown("✅ 点击下方空白行添加新用户")
st.markdown("✅ 直接点击要修改的单元格对已有用户的信息进行修改")
st.markdown("❌️ 对uid的修改是不被允许的")

df = DBusers.select_users()
df = pd.DataFrame(df)
df_key = 'users_key'

# df['password'] = df['password'].apply(md5_encrypt)
if df_key not in st.session_state:
    st.session_state[df_key] = df

df_editor_key = get_editor_key(df_key)

person_editor = st.data_editor(
    st.session_state[df_key],
    column_config={
        "uid": st.column_config.TextColumn(
            label="uid",
            max_chars=45,
            validate="^[0-9a-zA-Z!@#\$%^&*()\\.,-]+$",
            required=True,
        ),
        "password": st.column_config.TextColumn(
            label="password",
            max_chars=45,
            validate="^[0-9a-zA-Z!@#\$%^&*()\\.,-]+$",
            required=True,
        ),
        "admin": st.column_config.TextColumn(
            label="auth",
            max_chars=1,
            default='0',
            validate="^[0-2]",
            required=True,
        )
    },
    use_container_width=True,
    num_rows="dynamic",
    disabled="False",
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
        uid = df.loc[df.index[idx], 'uid']
        password = None
        admin = None
        for name, value in row.items():
            if name == 'uid':
                continue
            if name == 'password':
                password = value
            if name == 'admin':
                admin = value
            df0.loc[df0.index[idx], name] = value
        DBusers.update_users(uid, password, admin)

    for idx in deleted_rows:
        uid = df.loc[df.index[idx], 'uid']
        DBusers.delete_users(uid)
    df0.drop(df0.index[deleted_rows], inplace=True)

    ss = []
    has_index = add_rows and '_index' in add_rows[0]
    for add_row in add_rows:
        DBusers.insert_users(add_row['uid'], add_row['password'], add_row['admin'])
        # add_row['password'] = md5_encrypt(add_row['password'])
        if '_index' in add_row:
            ss.append(pd.Series(data=add_row, name=add_row.pop('_index')))
        else:
            ss.append(pd.Series(data=add_row))

    df_add = pd.DataFrame(ss)

    return pd.concat([df0, df_add], axis=0) if has_index else pd.concat([df0, df_add], axis=0, ignore_index=True)


if st.button("提交修改"):
    data_editor_change(df_key, df_editor_key)
    st.success("用户信息修改成功")
