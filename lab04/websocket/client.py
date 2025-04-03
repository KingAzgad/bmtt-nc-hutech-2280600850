import tornado.ioloop
import tornado.websocket

class WebSocketClient:
    def __init__(self, io_loop):
        self.connection = None
        self.io_loop = io_loop
        self.retry_count = 0
        self.max_retries = 5

    def start(self):
        self.connect_and_read()

    def stop(self):
        if self.connection:
            self.connection.close()
        self.io_loop.stop()

    async def connect_and_read(self):
        while self.retry_count < self.max_retries:
            try:
                print("Attempting to connect...")
                self.connection = await tornado.websocket.websocket_connect(
                    url="ws://localhost:8888/websocket",
                    ping_interval=10,
                    ping_timeout=30
                )
                print("Connected successfully!")
                self.retry_count = 0
                await self.read_messages()
            except Exception as e:
                self.retry_count += 1
                print(f"Connection failed: {e}")
                print(f"Retrying in 3 seconds... (Attempt {self.retry_count}/{self.max_retries})")
                await tornado.gen.sleep(3)
        
        if self.retry_count >= self.max_retries:
            print("Max retries reached. Giving up.")
            self.stop()

    async def read_messages(self):
        while True:
            try:
                message = await self.connection.read_message()
                if message is None:  # Connection closed
                    print("Connection closed by server")
                    self.connection = None
                    await self.connect_and_read()
                    break
                print(f"Received message from server: {message}")
            except Exception as e:
                print(f"Error reading message: {e}")
                self.connection = None
                await self.connect_and_read()
                break

def main():
    io_loop = tornado.ioloop.IOLoop.current()
    client = WebSocketClient(io_loop)
    
    io_loop.spawn_callback(client.connect_and_read)
    io_loop.start()

if __name__ == "__main__":
    main()