"""测试 psycopg2 的 RealDictCursor 返回值"""
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

# 模拟API代码
cursor.execute("SELECT * FROM campaigns WHERE id = %s", ("892def08-665c-4436-8176-1d3bb8db4bd9",))
row = cursor.fetchone()
print("campaigns row 类型:", type(row))
print("campaigns row 字段:", list(row.keys()) if row else None)

if row:
    print("\n=== 查询模拟结果 ===")
    cursor.execute("""
        SELECT variant_results, metrics, summary, timestamp
        FROM simulation_results
        WHERE campaign_id = %s
        ORDER BY timestamp DESC LIMIT 1
    """, ("892def08-665c-4436-8176-1d3bb8db4bd9",))
    result_row = cursor.fetchone()
    print("result_row 类型:", type(result_row))

    if result_row:
        print("\nresult_row 字段:", list(result_row.keys()))
        for key, value in result_row.items():
            print(f"  {key}: 类型={type(value).__name__}, 值={str(value)[:200]}")

conn.close()
