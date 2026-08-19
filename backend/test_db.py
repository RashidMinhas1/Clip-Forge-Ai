import asyncio, asyncpg

async def run():
    conn = await asyncpg.connect('postgresql://postgres.epcxaiztuvgwrafrkouu:WqcFpfvmfAxBsy6M@aws-0-ap-southeast-1.pooler.supabase.com:5432/postgres')
    print(await conn.fetch('SELECT * FROM auth.users LIMIT 5'))
    await conn.close()

asyncio.run(run())
