import streamlit as st
import pandas as pd
from db import run_query, run_query_df
import db

def update_dispute(dispute_id, new_status, new_note):
    conn = db.init_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT target_type, target_id FROM `dispute` WHERE id = %s", (dispute_id,))
        record = cursor.fetchone()
        
        query = """
            UPDATE `dispute`
            SET status = %s, admin_note = %s
            WHERE id = %s
        """
        cursor.execute(query, (new_status, new_note, dispute_id))
        
        # 联动控制：如果已处罚，且举报对象是商品，直接屏蔽商品
        if record and new_status == '已处罚' and record['target_type'] == '商品':
            cursor.execute("UPDATE `goods` SET status = 'BANNED' WHERE id = %s", (record['target_id'],))
            
        conn.commit()

def render():
    st.header("⚖️ 实时待办监控与处理工作台")
    
    # 待办数据卡片
    stats_query = """
        SELECT 
            COUNT(*) as pending_count,
            AVG(TIMESTAMPDIFF(HOUR, create_time, update_time)) as avg_handle_hours
        FROM `dispute`
        WHERE status = '待处理' OR status = '处理中'
    """
    df_stats = run_query_df(stats_query)
    
    col1, col2 = st.columns(2)
    with col1:
        count = df_stats.iloc[0]['pending_count'] if not df_stats.empty else 0
        st.metric("待处理纠纷单总数", count)
    with col2:
        hours = df_stats.iloc[0]['avg_handle_hours'] if not df_stats.empty and pd.notnull(df_stats.iloc[0]['avg_handle_hours']) else 0
        st.metric("平均响应耗时", f"{float(hours):.1f} 小时")
        
    import streamlit_antd_components as sac
    
    st.divider()
    st.subheader("📋 快捷处理列表")
    
    tab = sac.tabs([
        sac.TabsItem(label='待处理', icon='clock'),
        sac.TabsItem(label='已处理', icon='check-circle'),
    ], size='sm')
    
    # 获取待处理列表
    disputes_query = """
        SELECT 
            id, reporter_id, target_type, target_id, reason, status, create_time, evidence_img, admin_note
        FROM `dispute`
        ORDER BY FIELD(status, '待处理', '处理中', '已处罚', '已驳回'), create_time DESC
    """
    df_disputes = run_query_df(disputes_query)
    
    if df_disputes.empty:
        st.info("当前没有纠纷记录")
        return
        
    if tab == '待处理':
        df_show = df_disputes[df_disputes['status'].isin(['待处理', '处理中'])]
    else:
        df_show = df_disputes[df_disputes['status'].isin(['已处罚', '已驳回'])]

    if df_show.empty:
        st.info("当前分类下没有纠纷记录")
    else:
        # 展示简化版表格
        st.dataframe(
            df_show[['id', 'reporter_id', 'target_type', 'target_id', 'status', 'create_time']],
            use_container_width=True
        )
    
    # 工作台操作区
    st.subheader("🛠️ 纠纷处理区")
    
    if not df_show.empty:
        selected_id = st.selectbox("选择要处理的纠纷单 ID", df_show['id'].tolist())
    else:
        selected_id = None
    
    if selected_id:
        record = df_disputes[df_disputes['id'] == selected_id].iloc[0]
        
        with st.container(border=True):
            st.markdown(f"**纠纷单号**: #{record['id']} | **举报人**: User {record['reporter_id']}")
            st.markdown(f"**举报对象**: {record['target_type']} (ID: {record['target_id']})")
            st.markdown(f"**举报原因**: {record['reason']}")
            
            if record['evidence_img'] and isinstance(record['evidence_img'], str):
                st.write("**证据截图:**")
                try:
                    # 如果本地有图片展示图片
                    st.image(record['evidence_img'], width=300)
                except Exception as e:
                    st.warning(f"图片加载失败，路径: {record['evidence_img']}")
            
            with st.form(key=f"handle_form_{selected_id}"):
                new_status = st.selectbox("修改状态", ['待处理', '处理中', '已处罚', '已驳回'], index=['待处理', '处理中', '已处罚', '已驳回'].index(record['status']))
                new_note = st.text_area("管理员内部备注（如处罚理由）", value=record['admin_note'] if pd.notnull(record['admin_note']) else "")
                
                submit = st.form_submit_button("保存处理结果", type="primary")
                if submit:
                    update_dispute(selected_id, new_status, new_note)
                    st.success(f"纠纷单 #{selected_id} 处理成功！")
                    st.rerun()
