import pymysql
import pandas as pd
import streamlit as st
import configparser
import os

@st.cache_resource
def init_connection():
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
    config.read(config_path)
    
    return pymysql.connect(
        host=config.get('mysql', 'host'),
        port=config.getint('mysql', 'port'),
        user=config.get('mysql', 'user'),
        password=config.get('mysql', 'password'),
        database=config.get('mysql', 'database'),
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )

def run_query(query, params=None):
    conn = init_connection()
    # Ping to reconnect if connection timed out
    conn.ping(reconnect=True)
    with conn.cursor() as cursor:
        cursor.execute(query, params)
        if query.strip().upper().startswith("SELECT"):
            return cursor.fetchall()
        return []

def run_query_df(query, params=None):
    """返回 pandas DataFrame 格式的查询结果"""
    res = run_query(query, params)
    return pd.DataFrame(res)
