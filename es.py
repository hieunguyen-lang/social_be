from app.helpers import request_get_data

import asyncio

async def main():
    await request_get_data.get_request_data_instagram("vietnam")

asyncio.run(main())
