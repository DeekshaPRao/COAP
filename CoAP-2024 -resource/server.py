import aiocoap.resource as resource
import aiocoap
import asyncio

from aiocoap.numbers.contentformat import ContentFormat

import datetime


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

class TimeResource(resource.ObservableResource):
    """Example resource that can be observed. The `notify` method keeps
    scheduling itself, and calles `updated_state` to trigger sending
    notifications."""

    def __init__(self):
        super().__init__()

        self.handle = None

    def notify(self):
        self.updated_state()
        self.reschedule()

    def reschedule(self):
        self.handle = asyncio.get_event_loop().call_later(5, self.notify)

    def update_observation_count(self, count):
        if count and self.handle is None:
            print("Starting the clock")
            self.reschedule()
        if count == 0 and self.handle:
            print("Stopping the clock")
            self.handle.cancel()
            self.handle = None

    async def render_get(self, request):
        payload = datetime.datetime.now().strftime("%Y-%m-%d %H:%M").encode("ascii")
        return aiocoap.Message(payload=payload)


class WhoAmI(resource.Resource):
    async def render_get(self, request):
        text = ["Used protocol: %s." % request.remote.scheme]

        text.append("Request came from %s." % request.remote.hostinfo)
        text.append("The server address used %s." % request.remote.hostinfo_local)

        claims = list(request.remote.authenticated_claims)
        if claims:
            text.append(
                "Authenticated claims of the client: %s."
                % ", ".join(repr(c) for c in claims)
            )
        else:
            text.append("No claims authenticated.")

        return aiocoap.Message(content_format=0, payload="\n".join(text).encode("utf8"))


def main():
    # Resource tree creation
    root = resource.Site()

    root.add_resource(
        [".well-known", "core"], resource.WKCResource(root.get_resources_as_linkheader)
    )
    root.add_resource(['alarm'], AlarmResource())
    root.add_resource(["whoami"], WhoAmI())
    root.add_resource(["time"], TimeResource())
    #await aiocoap.Context.create_server_context(root,bind=('192.168.29.10', 5683))
    asyncio.Task(aiocoap.Context.create_server_context(root, bind=('10.114.241.44', 5683)))

    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    main()