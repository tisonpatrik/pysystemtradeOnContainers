import asyncpg

class Database:
    def __init__(self, test_database_url):
        self.test_database_url = test_database_url
        self.pool = None

    async def connect(self):
        if self.pool is None:
            self.pool = await asyncpg.create_pool(self.test_database_url)
        else:
            print("Pool already initialized")

    async def close(self):
        if self.pool:
            await self.pool.close()
            self.pool = None
        else:
            print("No pool to close")

    async def get_conn(self):
        if self.pool:
            return await self.pool.acquire()
        else:
            raise AttributeError("Pool not initialized")

    async def release_conn(self, conn):
        if self.pool:
            await self.pool.release(conn)
        else:
            raise AttributeError("Pool not initialized")
