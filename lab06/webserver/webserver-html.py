import socket
import os

def handle_request(client_socket, request_data):

    if "GET /admin" in request_data:
        file_name = "admin.html"
    else:
        file_name = "index.html"

    file_path = os.path.join(os.path.dirname(__file__), file_name)
    if not os.path.exists(file_path):
        response = "HTTP/1.1 404 Not Found\r\nContent-Type: text/html; charset=utf-8\r\n\r\n<h1>404 Not Found</h1>"
    else:
        response = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n"
        with open(file_path, "r", encoding='utf-8') as file:
            response += file.read()

    client_socket.sendall(response.encode('utf-8'))
    client_socket.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 8080))
    server_socket.listen(5)

    print("Server listening on port 8080...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")
        request_data = client_socket.recv(1024).decode('utf-8')
        handle_request(client_socket, request_data)

if __name__ == "__main__":
    main()
