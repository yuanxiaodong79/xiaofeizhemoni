import psycopg2

try:
    conn = psycopg2.connect(
        host='localhost',
        port=5432,
        database='marketing_windtunnel',
        user='postgres',
        password='postgres'
    )
    cur = conn.cursor()
    
    cur.execute('SELECT id, name, type, status, agent_count, created_at FROM campaigns')
    rows = cur.fetchall()
    
    print('=' * 80)
    print('数据库 campaigns 表记录')
    print('=' * 80)
    
    if not rows:
        print('无记录')
    else:
        print(f'共 {len(rows)} 条记录')
        print('-' * 80)
        for r in rows:
            print(f'ID:         {r[0]}')
            print(f'名称:       {r[1]}')
            print(f'类型:       {r[2]}')
            print(f'状态:       {r[3]}')
            print(f'智能体数:   {r[4]}')
            print(f'创建时间:   {r[5]}')
            print('-' * 80)
    
    conn.close()
except Exception as e:
    print(f'查询失败: {e}')