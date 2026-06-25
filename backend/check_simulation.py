"""检查 simulation_results 表的具体数据"""
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

# 查询字段类型
cursor.execute("""
    SELECT column_name, data_type FROM information_schema.columns
    WHERE table_name = 'simulation_results' ORDER BY ordinal_position
""")
print("=== simulation_results 字段类型 ===")
for row in cursor.fetchall():
    print(f"  {row['column_name']}: {row['data_type']}")

# 直接查询刚才那个campaign的模拟结果
print("\n=== 查询 campaign 892def08 的所有结果 ===")
cursor.execute("""
    SELECT * FROM simulation_results
    WHERE campaign_id = '892def08-665c-4436-8176-1d3bb8db4bd9'
    ORDER BY timestamp DESC
""")
rows = cursor.fetchall()
print(f"查询到 {len(rows)} 条记录")
for row in rows:
    print(f"\n记录ID: {row['id']}")
    print(f"campaign_id: {row['campaign_id']}")
    print(f"variant_results 类型: {type(row['variant_results'])}")
    print(f"variant_results 长度: {len(row['variant_results']) if row['variant_results'] else 0}")

# 也查询 campaigns 表中的ID格式
cursor.execute("SELECT id, name FROM campaigns WHERE name = '护肤品广告实验'")
print("\n=== campaigns 表中护肤品广告实验 ===")
for row in cursor.fetchall():
    print(f"  ID: {row['id']} 类型: {type(row['id'])}")

conn.close()
