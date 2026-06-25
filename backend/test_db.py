import psycopg2
import json

try:
    conn = psycopg2.connect(
        host='localhost',
        port=5432,
        database='marketing_windtunnel',
        user='postgres',
        password='postgres'
    )
    cur = conn.cursor()
    
    # 测试插入
    variants = [{'id': 'A', 'title': 'Test', 'description': 'Test', 'price': 100}]
    target_audience = {'persona_types': ['all']}
    
    cur.execute(
        """INSERT INTO campaigns (name, type, variants, target_audience, agent_count, status)
           VALUES (%s, %s, %s, %s, %s, %s) RETURNING *""",
        ('Test Campaign', 'ab_test', json.dumps(variants), json.dumps(target_audience), 100, 'draft')
    )
    
    row = cur.fetchone()
    conn.commit()
    print('Inserted:', row)
    
    # 查询所有记录
    cur.execute('SELECT id, name, type, status, agent_count, created_at FROM campaigns')
    rows = cur.fetchall()
    print('\nCampaigns:')
    for r in rows:
        print(f'ID: {r[0]}, Name: {r[1]}, Type: {r[2]}, Status: {r[3]}, Agents: {r[4]}, Created: {r[5]}')
    
    conn.close()
except Exception as e:
    print(f'Error: {e}')