import aiocoap.resource as resource
import aiocoap
import asyncio
from aiocoap.numbers import media_types_rev

# Alarm resource definition
class AlarmResource(resource.Resource):

    def __init__(self):
        super().__init__()
        self.state = b"OFF"

    async def render_get(self, request):
        payload = self.state
        print('Return alarm state: ', self.state)
        return aiocoap.Message(payload=payload)

    async def render_put(self, request):
        self.state = request.payload
        print('Update alarm state: ', self.state)
        return aiocoap.Message(code=aiocoap.CHANGED, payload=self.state)

# MyResource definition with well-known attributes
class MyResource(resource.Resource, resource._ExposesWellknownAttributes):
    def __init__(self):
        super().__init__()
        # Define the well-known attributes for this resource
        self.rt = "example-rt"  # Resource type
        self.if_ = "example-if"  # Interface description
        self.ct = media_types_rev['text/plain']  # Content type

    async def render_get(self, request):
        payload = b"This is the response payload"
        return aiocoap.Message(code=aiocoap.CONTENT, payload=payload)

# Main function to set up the CoAP server
def main():
    # Resource tree creation
    root = resource.Site()

    # Add the alarm resource
    root.add_resource(['alarm'], AlarmResource())

    # Add the resource with well-known attributes
    root.add_resource(('my-resource',), MyResource())

    # Add the .well-known/core resource for discovery
    root.add_resource(('.well-known/core',), resource.WKCResource(root.get_resources_as_linkheader))

    # Create server context and run the event loop
    asyncio.Task(aiocoap.Context.create_server_context(root, bind=('192.168.29.10', 5683)))
    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    main()
