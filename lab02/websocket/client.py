import tornado.ioloop
import tornado.websocket
import asyncio

class WebSocketClient:
    def __init__(self, io_loop):
        self.io_loop = io_loop
        self.connection = None
        self.url = "ws://localhost:8888/websocket"

    async def connect(self):
        print("Connecting...")
        try:
            self.connection = await tornado.websocket.websocket_connect(self.url)
            print("Connected to server.")
            await self.read_message()
        except Exception as e:
            print(f"Could not reconnect, retrying in 3 seconds... Error: {e}")
            self.io_loop.call_later(3, lambda: asyncio.ensure_future(self.connect()))

    async def read_message(self):
        while True:
            try:
                message = await self.connection.read_message()
                if message is None:
                    print("Server disconnected, reconnecting...")
                    await self.connect()
                    break
                print(f"Received from server: {message}")
            except Exception as e:
                print(f"Error reading message: {e}")
                break

def main():
    io_loop = tornado.ioloop.IOLoop.current()
    client = WebSocketClient(io_loop)
    asyncio.ensure_future(client.connect())
    io_loop.start()

if __name__ == "__main__":
    main()
