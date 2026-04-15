import streamlit as st
import pandas as pd
from db import run_query_df

def render():
    st.header("🧾 全局订单安全审计")
    
    st.markdown("这里是所有交易的汇集地。无论暗流涌动，所有订单编号皆有迹可循。")
    st.divider()

    query = """
        SELECT o.id, o.order_no, o.good_name, o.total, o.status, o.create_time,
               b.name as buyer_name, s.name as seller_name
        FROM `order` o
        JOIN `user` b ON o.user_id = b.id
        JOIN `user` s ON o.sale_id = s.id
        ORDER BY o.create_time DESC
    """
    df = run_query_df(query)
    
    if df.empty:
        st.info("当前平台没有产生任何订单流水")
        return
        
    st.dataframe(
        df[['id', 'order_no', 'good_name', 'total', 'status', 'buyer_name', 'seller_name', 'create_time']],
        use_container_width=True
    )
    
    st.markdown("> **⚠️ 提示**: 管理端仅供调阅审计订单流，不可篡改金额以保障交易一致性。若对交易有疑问可通过纠纷工作台退款。")
