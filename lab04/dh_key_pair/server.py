from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives import serialization

def main():
    parameters = dh.generate_parameters(generator=2, key_size=2048)
    private_key = parameters.generate_private_key()
    public_key = private_key.public_key()

    with open("C:\\bmtt-nc-hutech-2280600850\\lab04\\dh_key_pair\\server_public_key.pem", "wb") as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))
    print("Khóa công khai đã được ghi vào server_public_key.pem")

if __name__ == "__main__":
    print("Chương trình bắt đầu...")
    main()
    print("Chương trình kết thúc.")