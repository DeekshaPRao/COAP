import asyncio
import random

from aiocoap import *

async def main():
    context = await Context.create_client_context()

    request = Message(code=GET,  uri="coap://10.114.241.44/.well-known/core")
    response = await context.request(request).response
    print('Result: ', response.code, response.payload)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())