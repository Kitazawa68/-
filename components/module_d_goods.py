import streamlit as st
import pandas as pd
from db import run_query_df
import db

def toggle_goods_status(good_id, current_status):
    new_status = 'OFF_SALE' if current_status == 'ON_SALE' else 'ON_SALE'
    conn = db.init_connection()
    with conn.cursor() as cursor:
        cursor.execute("UPDATE `goods` SET status = %s WHERE id = %s", (new_status, good_id))
        conn.commit()

def render():
    st.header("🗃️ 全局商品库管理")
    
    st.markdown("在这里，你可以纵览全平台的所有二手商品，并对涉嫌违规的商品进行**紧急下架**操作。")
    st.divider()

    # Query goods
    query = """
        SELECT g.id, g.name, g.price, g.status, u.username, u.name as seller_name, g.content
        FROM `goods` g
        JOIN `user` u ON g.user_id = u.id
        ORDER BY g.id DESC
    """
    df = run_query_df(query)
    
    if df.empty:
        st.info("当前平台毫无商品数据")
        return
        
    st.dataframe(
        df[['id', 'name', 'price', 'status', 'username', 'seller_name']],
        use_container_width=True
    )
    
    st.subheader("🛠️ 强制状态干预")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        selected_id = st.selectbox("请选择目标商品 ID", df['id'].tolist())
    
    if selected_id:
        record = df[df['id'] == selected_id].iloc[0]
        with col2:
            st.info(f"商品名称: **{record['name']}** | 卖家: {record['seller_name']}")
            st.text(f"简介: {record['content'][:50]}...")
            
            btn_text = "⚠️ 强制下架该商品" if record['status'] == 'ON_SALE' else "✅ 恢复无罪上架"
            btn_type = "primary" if record['status'] != 'ON_SALE' else "secondary"
            
            if st.button(btn_text, type=btn_type):
                toggle_goods_status(selected_id, record['status'])
                st.success(f"已成功更改商品 #{selected_id} 状态！")
                st.rerun()
