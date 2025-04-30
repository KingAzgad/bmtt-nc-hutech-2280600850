from Crypto.Hash import SHA3_256
def  sha3(message):
    hash_obj = SHA3_256.new()
    hash_obj.update(message)
    return hash_obj.hexdigest()
def main():
    message = input("Nhập ký tự cần băm: ").encode('utf-8')
    print(f"SHA3-256 băm của '{message.decode('utf-8')}': {sha3(message)}")
if __name__ == "__main__":
    main()