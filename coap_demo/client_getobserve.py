import asyncio
import random

from aiocoap import *

async def main():
    protocol = await Context.create_client_context()

    request = Message(code=GET,  uri="coap://192.168.29.10/obs", observe=0)
    pr = protocol.request(request)

    r = await pr.response
    print("First response: %s\n%r" % (r, r.payload))

    async for r in pr.observation:
        print("Next result: %s\n%r" % (r, r.payload))

        pr.observation.cancel()
        break
    print("Loop ended, sticking around")
    await asyncio.sleep(50)



if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())