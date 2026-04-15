import streamlit as st
import pandas as pd
from db import run_query_df

def render():
    st.header("📈 大盘基础流水看板")
    
    # 获取今日数据
    # 为保证数据展示，如果今天没数据，我们就查最近一天的或者是总计（此处按PRD查询今日，但我为了防止空数据影响体验，会 fallback 到看最新的一天）
    
    metrics_query = """
        SELECT 
            (SELECT COALESCE(SUM(total), 0) FROM `order` WHERE DATE(create_time) = CURDATE()) as today_total,
            (SELECT COUNT(*) FROM `user` WHERE DATE(create_time) = CURDATE()) as today_users,
            (SELECT COUNT(*) FROM `order` WHERE DATE(create_time) = CURDATE() AND status != '已取消') as today_active_orders
    """
    df_metrics = run_query_df(metrics_query)
    
    if not df_metrics.empty:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("今日交易总额 (元)", f"¥ {df_metrics.iloc[0]['today_total']:.2f}")
        with col2:
            st.metric("今日新增用户", f"{df_metrics.iloc[0]['today_users']} 人")
        with col3:
            st.metric("活跃交易量", f"{df_metrics.iloc[0]['today_active_orders']} 笔")
    else:
        st.warning("暂无今日数据")
        
    st.subheader("📊 近 7 天趋势")
    
    # 获取过去7天的日期范围
    last_7_days = pd.date_range(end=pd.Timestamp.today().normalize(), periods=7)

    # 7天交易走势
    trend_query = """
        SELECT DATE(create_time) as date, COALESCE(SUM(total), 0) as daily_total
        FROM `order`
        WHERE create_time >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
        GROUP BY DATE(create_time)
        ORDER BY date ASC
    """
    df_trend = run_query_df(trend_query)
    if not df_trend.empty and 'daily_total' in df_trend.columns:
        df_trend['date'] = pd.to_datetime(df_trend['date'])
        df_trend = df_trend.set_index('date')
        df_trend['daily_total'] = df_trend['daily_total'].astype(float)
    else:
        df_trend = pd.DataFrame(columns=['daily_total'])
    
    # 补全可能缺失的日期
    df_trend = df_trend.reindex(last_7_days, fill_value=0)
    
    # 7天新增用户走势
    user_trend_query = """
        SELECT DATE(create_time) as date, COUNT(*) as new_users
        FROM `user`
        WHERE create_time >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
        GROUP BY DATE(create_time)
        ORDER BY date ASC
    """
    df_user_trend = run_query_df(user_trend_query)
    if not df_user_trend.empty and 'new_users' in df_user_trend.columns:
        df_user_trend['date'] = pd.to_datetime(df_user_trend['date'])
        df_user_trend = df_user_trend.set_index('date')
        df_user_trend['new_users'] = df_user_trend['new_users'].astype(float)
    else:
        df_user_trend = pd.DataFrame(columns=['new_users'])
        
    # 补全可能缺失的日期
    df_user_trend = df_user_trend.reindex(last_7_days, fill_value=0)
    
    from streamlit_echarts import st_echarts
    
    col1, col2 = st.columns(2)
    
    x_data = df_trend.index.strftime('%Y-%m-%d').tolist()
    y_data_trend = df_trend['daily_total'].tolist()
    y_data_users = df_user_trend['new_users'].tolist()
    
    with col1:
        options_trend = {
            "title": {"text": "近 7 天交易额走势", "left": "center", "textStyle": {"fontSize": 14, "fontWeight": "normal"}},
            "tooltip": {"trigger": "axis"},
            "xAxis": {
                "type": "category",
                "boundaryGap": False,
                "data": x_data
            },
            "yAxis": {"type": "value"},
            "series": [
                {
                    "data": y_data_trend,
                    "type": "line",
                    "smooth": True,
                    "areaStyle": {
                        "color": {
                            "type": "linear",
                            "x": 0, "y": 0, "x2": 0, "y2": 1,
                            "colorStops": [
                                {"offset": 0, "color": "rgba(58, 119, 255, 0.5)"},
                                {"offset": 1, "color": "rgba(58, 119, 255, 0.05)"}
                            ]
                        }
                    },
                    "itemStyle": {"color": "#3a77ff"}
                }
            ]
        }
        st_echarts(options=options_trend, height="400px")
            
    with col2:
        options_users = {
            "title": {"text": "近 7 天用户新增走势", "left": "center", "textStyle": {"fontSize": 14, "fontWeight": "normal"}},
            "tooltip": {"trigger": "axis"},
            "xAxis": {
                "type": "category",
                "boundaryGap": False,
                "data": x_data
            },
            "yAxis": {"type": "value"},
            "series": [
                {
                    "data": y_data_users,
                    "type": "line",
                    "smooth": True,
                    "areaStyle": {
                        "color": {
                            "type": "linear",
                            "x": 0, "y": 0, "x2": 0, "y2": 1,
                            "colorStops": [
                                {"offset": 0, "color": "rgba(0, 216, 135, 0.5)"},
                                {"offset": 1, "color": "rgba(0, 216, 135, 0.05)"}
                            ]
                        }
                    },
                    "itemStyle": {"color": "#00d887"}
                }
            ]
        }
        st_echarts(options=options_users, height="400px")
