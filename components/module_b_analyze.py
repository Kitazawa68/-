import streamlit as st
import pandas as pd
from db import run_query_df

def render():
    st.header("🎯 平台健康度画像")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("⚠️ 高风险举报分布 (Top 5 类别)")
        
        type_query = """
            SELECT target_type, COUNT(*) as report_count
            FROM `dispute`
            GROUP BY target_type
            ORDER BY report_count DESC
            LIMIT 5
        """
        df_type = run_query_df(type_query)
        from streamlit_echarts import st_echarts
        if not df_type.empty:
            pie_data = [{"value": int(row['report_count']), "name": str(row['target_type'])} for index, row in df_type.iterrows()]
            options_pie = {
                "tooltip": {"trigger": "item"},
                "legend": {"bottom": 0, "left": "center"},
                "series": [
                    {
                        "name": "举报类别",
                        "type": "pie",
                        "radius": ["40%", "70%"],
                        "avoidLabelOverlap": False,
                        "itemStyle": {
                            "borderRadius": 10,
                            "borderColor": "#fff",
                            "borderWidth": 2
                        },
                        "label": {"show": False, "position": "center"},
                        "emphasis": {
                            "label": {"show": True, "fontSize": "20", "fontWeight": "bold"}
                        },
                        "labelLine": {"show": False},
                        "data": pie_data,
                        "color": ["#5470c6", "#91cc75", "#fac858", "#ee6666", "#73c0de"]
                    }
                ]
            }
            st_echarts(options=options_pie, height="350px")
        else:
            st.info("暂无举报类别数据")
            
    with col2:
        st.subheader("🕵️ 高危用户排行 (Top 5)")
        target_query = """
            SELECT CONCAT(target_type, ' #', target_id) as target_name, COUNT(*) as count
            FROM `dispute`
            GROUP BY target_type, target_id
            ORDER BY count DESC
            LIMIT 5
        """
        df_target = run_query_df(target_query)
        if not df_target.empty:
            df_target = df_target.sort_values(by='count', ascending=True) # Echarts horizontal bar reads from bottom up
            y_data = df_target['target_name'].tolist()
            x_data = df_target['count'].tolist()
            options_bar = {
                "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
                "grid": {"left": "3%", "right": "4%", "bottom": "3%", "containLabel": True},
                "xAxis": {"type": "value", "boundaryGap": [0, 0.01]},
                "yAxis": {"type": "category", "data": y_data},
                "series": [
                    {
                        "name": "举报次数",
                        "type": "bar",
                        "data": x_data,
                        "itemStyle": {
                            "borderRadius": [0, 5, 5, 0],
                            "color": "rgba(255, 107, 107, 0.8)"
                        }
                    }
                ]
            }
            st_echarts(options=options_bar, height="350px")
        else:
            st.info("暂无高危对象数据")
            
    st.divider()
    st.subheader("🌪️ 举报有效转化漏斗")
    
    funnel_query = """
        SELECT
            (SELECT COUNT(*) FROM `dispute`) as total_reports,
            (SELECT COUNT(*) FROM `dispute` WHERE status IN ('处理中', '已处罚', '已驳回')) as handled_reports,
            (SELECT COUNT(*) FROM `dispute` WHERE status = '已处罚') as penalty_reports
    """
    df_funnel = run_query_df(funnel_query)
    
    if not df_funnel.empty and df_funnel.iloc[0]['total_reports'] > 0:
        total = int(df_funnel.iloc[0]['total_reports'])
        handled = int(df_funnel.iloc[0]['handled_reports'])
        penalty = int(df_funnel.iloc[0]['penalty_reports'])
        
        col_text, col_chart = st.columns([1, 2])
        
        with col_text:
            st.metric("总体处理率", f"{handled / total * 100:.1f}%")
            st.metric("确认违规率 (实锤率)", f"{penalty / total * 100:.1f}%")
            
            if penalty / total < 0.1 and total > 10:
                st.warning("提示：处罚率偏低，建议人工复核是否存在恶意批量举报行为。")
                
        with col_chart:
            funnel_data = [
                {"value": total, "name": "收到举报"},
                {"value": handled, "name": "处理受理"},
                {"value": penalty, "name": "核实处罚"}
            ]
            options_funnel = {
                "tooltip": {"trigger": "item", "formatter": "{a} <br/>{b} : {c}"},
                "toolbox": {"feature": {"dataView": {"readOnly": False}, "restore": {}, "saveAsImage": {}}},
                "series": [
                    {
                        "name": "举报转化漏斗",
                        "type": "funnel",
                        "left": "10%",
                        "top": 20,
                        "bottom": 20,
                        "width": "80%",
                        "min": 0,
                        "max": total,
                        "minSize": "0%",
                        "maxSize": "100%",
                        "sort": "descending",
                        "gap": 2,
                        "label": {"show": True, "position": "inside"},
                        "labelLine": {"length": 10, "lineStyle": {"width": 1, "type": "solid"}},
                        "itemStyle": {"borderColor": "#fff", "borderWidth": 1},
                        "emphasis": {"label": {"fontSize": 20}},
                        "data": funnel_data,
                        "color": ["#8a2be2", "#4169e1", "#ff6347"]
                    }
                ]
            }
            st_echarts(options=options_funnel, height="300px")
            
    else:
        st.info("暂无漏斗数据")
