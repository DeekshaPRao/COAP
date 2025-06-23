import asyncio
import random

from aiocoap import *

async def main():
    context = await Context.create_client_context()
    alarm_state = random.choice([True, False])
    payload = b"OFF"

    if alarm_state:
        payload = b"ON"

    request = Message(code=PUT, payload=payload, uri="coap://192.168.29.10/alarm")

    response = await context.request(request).response
    print('Result: ', response.code, response.payload)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())