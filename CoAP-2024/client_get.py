import asyncio
import random

from aiocoap import *

async def main():
    protocol = await Context.create_client_context()

    request = Message(code=GET,  uri="coap://10.114.241.44/alarm")
    pr = protocol.request(request)

    r = await pr.response
    print('Result: ', r.code, r.payload)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())