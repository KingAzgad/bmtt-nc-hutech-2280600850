import socket
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import threading

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen(5)

my_key = RSA.generate(2048)  # Đổi tên server_key thành my_key

clients = []

def encrypt_text(key, msg):  # Đổi tên hàm và tham số
    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv 
    enc_data = cipher.encrypt(pad(msg.encode(), AES.block_size))  # Đổi tên biến
    return iv + enc_data 

def decrypt_text(key, enc_data):  # Đổi tên hàm và tham số
    iv = enc_data[:AES.block_size] 
    cipher_data = enc_data[AES.block_size:]  # Đổi tên biến
    cipher = AES.new(key, AES.MODE_CBC, iv)  
    plain_data = unpad(cipher.decrypt(cipher_data), AES.block_size)
    return plain_data.decode()

def handle_connection(cli_socket, cli_address):  # Đổi tên hàm và tham số
    print(f"Connection from {cli_address} has been established.")

    cli_socket.send(my_key.publickey().export_key(format='PEM'))

    cli_pub_key = RSA.import_key(cli_socket.recv(2048))  # Đổi tên client_received_key

    session_key = get_random_bytes(16)  # Đổi tên aes_key

    rsa_cipher = PKCS1_OAEP.new(cli_pub_key)  # Đổi tên cipher_rsa
    enc_session_key = rsa_cipher.encrypt(session_key)  # Đổi tên encrypted_aes_key
    cli_socket.send(enc_session_key)

    clients.append((cli_socket, session_key))

    while True:
        try:
            enc_msg = cli_socket.recv(1024)
            if not enc_msg:
                break

            plain_msg = decrypt_text(session_key, enc_msg)
            print(f"Received from {cli_address}: {plain_msg}")

            if plain_msg.lower() == "exit":
                break

            for client, key in clients:
                if client != cli_socket:
                    encrypted_data = encrypt_text(key, plain_msg)  # Đổi tên biến
                    client.send(encrypted_data)

        except Exception as e:
            print(f"Error with {cli_address}: {e}")
            break

    if (cli_socket, session_key) in clients:
        clients.remove((cli_socket, session_key))
    cli_socket.close()
    print(f"Connection with {cli_address} closed.")

while True:
    cli_socket, cli_address = server_socket.accept()
    cli_thread = threading.Thread(target=handle_connection, args=(cli_socket, cli_address))  # Đổi tên biến
    cli_thread.start()