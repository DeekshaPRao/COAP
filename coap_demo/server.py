import aiocoap.resource as resource
import aiocoap
import asyncio


class AlarmResource(resource.Resource):

    def __init__(self):
        super().__init__()
        self.state = b"OFF"

    async def render_get(self, request):
        payload=self.state
        print('Return alarm state: ', self.state)

        return aiocoap.Message(payload=payload)

    async def render_put(self, request):
        self.state = request.payload
        print('Update alarm state: ', self.state)

        return aiocoap.Message(code=aiocoap.CHANGED, payload=self.state)


def main():
    # Resource tree creation
    root = resource.Site()
    root.add_resource(['alarm'], AlarmResource())
 

    asyncio.Task(aiocoap.Context.create_server_context(root, bind=('192.168.29.10', 5683)))

    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    main()