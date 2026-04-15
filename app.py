import streamlit as st
import os

# Set page config
st.set_page_config(
    page_title="校园二手交易平台 - 管理后台",
    page_icon="🛒",
    layout="wide"
)

# Session State Authentication
import time

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    # Add a nice top margin and title
    st.markdown("<h2 style='text-align: center; margin-top: 100px;'>🛡️ 校园二手交易系统 - 监管中心</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.info("⚠️ 请输入系统安全密钥以获取监管后台访问权限。")
        password = st.text_input("安全密钥 (Password)", type="password")
        if st.button("授权登入 (Login)", use_container_width=True):
            if password == "admin123":
                st.success("✅ 密钥验证成功，正在进入系统...")
                st.session_state["authenticated"] = True
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("❌ 权限拒绝：无效的安全密钥！(Access Denied)")
    st.stop()


# Import components
try:
    from components import module_a_dispute, module_b_analyze, module_c_dashboard, module_d_goods, module_e_users, module_f_orders
    import db
except ImportError as e:
    st.error("组件加载失败，请确保所有文件结构正确。")
    st.stop()

# Check Database Connection
try:
    conn = db.init_connection()
except Exception as e:
    st.error("数据库连接失败！请运行 db_setup.py 或检查 config.ini 并在 MySQL 中启动服务。")
    st.exception(e)
    st.stop()

import streamlit_antd_components as sac

st.title("校园二手交易系统 - 管理中心 🛡️")

# Sidebar navigation
with st.sidebar:
    st.logo("🛒", icon_image="https://cdn-icons-png.flaticon.com/512/3144/3144456.png") # Add a logo placeholder
    
    page = sac.menu([
        sac.MenuItem('基础流水看板', icon='graph-up', description='Dashboard'),
        sac.MenuItem('实时待办监控', icon='kanban', description='纠纷工作台'),
        sac.MenuItem('平台健康度分析', icon='pie-chart', description='洞察板'),
        sac.MenuItem('全局商品库管理', icon='box', description='上下架干预'),
        sac.MenuItem('账号风控与用户管理', icon='people', description='监控/封禁'),
        sac.MenuItem('全局订单安全审计', icon='receipt', description='流水可溯源'),
    ], size='md', open_all=True)
    
    st.markdown("---")
    st.info("当前数据直连本地 MySQL 数据库。")

# Render selected page
if page == '基础流水看板':
    module_c_dashboard.render()
elif page == '实时待办监控':
    module_a_dispute.render()
elif page == '平台健康度分析':
    module_b_analyze.render()
elif page == '全局商品库管理':
    module_d_goods.render()
elif page == '账号风控与用户管理':
    module_e_users.render()
elif page == '全局订单安全审计':
    module_f_orders.render()
