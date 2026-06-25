"""查询数据库中的实验记录"""
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("DB_HOST", "localhost"),
    port=int(os.getenv("DB_PORT", 5432)),
    database=os.getenv("DB_NAME", "marketing_windtunnel"),
    user=os.getenv("DB_USER", "postgres"),
    password=os.getenv("DB_PASSWORD", "password"),
    cursor_factory=RealDictCursor
)
cursor = conn.cursor()

# 查询所有表
cursor.execute("""
    SELECT table_name FROM information_schema.tables
    WHERE table_schema='public' ORDER BY table_name
""")
print("=== 数据库所有表 ===")
tables = cursor.fetchall()
for row in tables:
    print(f"  {row['table_name']}")
print()

# 查询最近的实验记录
if any(t['table_name'] == 'campaigns' for t in tables):
    cursor.execute("""
        SELECT id, name, status, agent_count, created_at
        FROM campaigns ORDER BY created_at DESC LIMIT 10
    """)
    print("=== 最近的实验记录 ===")
    rows = cursor.fetchall()
    if rows:
        for row in rows:
            print(f"ID: {row['id']}")
            print(f"名称: {row['name']}")
            print(f"状态: {row['status']}")
            print(f"智能体数: {row['agent_count']}")
            print(f"时间: {row['created_at']}")
            print("---")
    else:
        print("没有实验记录")

# 查询 simulation_results 表
if any(t['table_name'] == 'simulation_results' for t in tables):
    cursor.execute("""
        SELECT id, campaign_id, used_llm, created_at
        FROM simulation_results ORDER BY created_at DESC LIMIT 5
    """)
    print("\n=== 最近的模拟结果 ===")
    rows = cursor.fetchall()
    if rows:
        for row in rows:
            print(f"ID: {row['id']}")
            print(f"实验ID: {row['campaign_id']}")
            print(f"使用LLM: {row['used_llm']}")
            print(f"时间: {row['created_at']}")
            print("---")
    else:
        print("没有模拟结果")

conn.close()
