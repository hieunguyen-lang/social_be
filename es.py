from app.helpers import request_get_data

import asyncio

async def main():
    a=await request_get_data.get_request_data_watchfb("đà%20nẵng")
    print(a)

asyncio.run(main())
