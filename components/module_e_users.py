import streamlit as st
import pandas as pd
from db import run_query_df
import db

def ban_user(user_id, is_banned):
    new_role = 'BANNED' if not is_banned else 'USER'
    conn = db.init_connection()
    with conn.cursor() as cursor:
        cursor.execute("UPDATE `user` SET role = %s WHERE id = %s", (new_role, user_id))
        conn.commit()

def render():
    st.header("👥 账号风控与用户管理")
    
    st.markdown("掌控平台的数字生态，随时识别风险账户并执行封禁。")
    st.divider()

    query = """
        SELECT id, username, name, phone, email, role, create_time 
        FROM `user`
        ORDER BY id DESC
    """
    df = run_query_df(query)
    
    if df.empty:
        st.info("当前平台没有用户")
        return
        
    # Stats
    banned_count = len(df[df['role'] == 'BANNED'])
    col_a, col_b = st.columns(2)
    col_a.metric("总注册人数", len(df))
    col_b.metric("已封停账号数", banned_count)
        
    st.dataframe(
        df[['id', 'username', 'name', 'phone', 'role', 'create_time']],
        use_container_width=True
    )
    
    st.subheader("⚖️ 账号风控区")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        selected_user = st.selectbox("选择目标用户 ID", df['id'].tolist())
    
    if selected_user:
        record = df[df['id'] == selected_user].iloc[0]
        with col2:
            is_banned = record['role'] == 'BANNED'
            st.info(f"账户: **{record['username']}** ({record['name']}) | 邮箱: {record['email']}")
            
            action_text = "🚫 解封该账号" if is_banned else "🚨 冻结封禁该账号"
            btn_type = "primary" if is_banned else "secondary"
            
            if st.button(action_text, type=btn_type):
                ban_user(selected_user, is_banned)
                st.success(f"已成功变更用户 #{selected_user} 风控状态！")
                st.rerun()
