import socket
import ssl
import threading

server_address = ('localhost', 12345)

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(
    certfile="C:\\bmtt-nc-hutech-2280600850\\lab05\\ssl\\certificates\\server-cert.crt",
    keyfile="C:/bmtt-nc-hutech-2280600850/lab05/ssl/certificates/server-key.key"
)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(server_address)
server_socket.listen(5)

print("Server chờ kết nối...")
clients = []

def handle_client(client_socket):
    clients.append(client_socket)
    print("Kết nối:", client_socket.getpeername())

    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            print("Nhận:", data.decode('utf-8'))
            for client in clients:
                if client != client_socket:
                    try:
                        client.send(data)
                    except:
                        clients.remove(client)
    except:
        clients.remove(client_socket)
    finally:
        print("Ngắt kết nối:", client_socket.getpeername())
        clients.remove(client_socket)
        client_socket.close()

while True:
    client_socket, client_address = server_socket.accept()
    ssl_socket = context.wrap_socket(client_socket, server_side=True)
    print(f"Kết nối từ {client_address}")
    threading.Thread(target=handle_client, args=(ssl_socket,)).start()