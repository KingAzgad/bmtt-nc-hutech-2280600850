import hashlib

def blake2(message):
    h = hashlib.blake2b()
    h.update(message.encode('utf-8'))
    return h.hexdigest()

if __name__ == "__main__":
    message = input("Enter a string to hash: ")
    print("BLAKE2 hash:", blake2(message))