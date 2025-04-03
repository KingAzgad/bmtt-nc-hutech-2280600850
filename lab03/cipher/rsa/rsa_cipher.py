import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.rsa import Ui_MainWindow
import requests

import rsa

class RSACipher:
    def __init__(self):
        self.private_key = None
        self.public_key = None

    def generate_keys(self):
        (self.public_key, self.private_key) = rsa.newkeys(512)
        with open("public.pem", "wb") as pub_file:
            pub_file.write(self.public_key.save_pkcs1("PEM"))
        with open("private.pem", "wb") as priv_file:
            priv_file.write(self.private_key.save_pkcs1("PEM"))

    def load_keys(self):
        try:
            with open("public.pem", "rb") as pub_file:
                public_key = rsa.PublicKey.load_pkcs1(pub_file.read())
            with open("private.pem", "rb") as priv_file:
                private_key = rsa.PrivateKey.load_pkcs1(priv_file.read())
            return private_key, public_key
        except FileNotFoundError:
            raise Exception("Key files not found. Please generate keys first.")

    # Thêm phương thức encrypt
    def encrypt(self, message, public_key):
        return rsa.encrypt(message.encode(), public_key)
    
    # Thêm phương thức decrypt
    def decrypt(self, ciphertext, private_key):
        return rsa.decrypt(ciphertext, private_key).decode()
    
    def sign(self, message, private_key):
        return rsa.sign(message.encode(), private_key, 'SHA-256')

    def verify(self, message, signature, public_key):
        """Xác minh chữ ký bằng public key"""
        try:
            rsa.verify(message.encode(), signature, public_key)
            return True
        except rsa.VerificationError:
            return False

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.btn_gen_key.clicked.connect(self.call_api_gen_keys)
        self.ui.btn_encrypt.clicked.connect(self.call_api_encrypt)
        self.ui.btn_decrypt.clicked.connect(self.call_api_decrypt)
        self.ui.btn_sign.clicked.connect(self.call_api_sign)
        self.ui.btn_verify.clicked.connect(self.call_api_verify) 
        
    def call_api_gen_keys(self):
        url = "http://127.0.0.1:5000/api/rsa/generate_keys"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText(data["message"])  
                msg.exec_()
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print("Error:%s" % e)
            
    def call_api_encrypt(self):
        url = "http://127.0.0.1:5000/api/rsa/encrypt"
        payload = {
            "message": self.ui.txt_plain_text.toPlainText(),
            "key_type": "public"
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_cipher_text.setPlainText(data["encrypted_message"])  
                
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Encryption Successful") 
                msg.exec_()
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print("Error:%s" % e)
            
    def call_api_decrypt(self):
        url = "http://127.0.0.1:5000/api/rsa/decrypt"  
        payload = {
            "ciphertext": self.ui.txt_cipher_text.toPlainText(),
            "key_type": "private"
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_plain_text.setPlainText(data["decrypted_message"]) 
                
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Decryption Successful")  
                msg.exec_()
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print("Error:%s" % e)
            
    def call_api_sign(self):
        url = "http://127.0.0.1:5000/api/rsa/sign" 
        payload = {
            "message": self.ui.txt_info.toPlainText(),
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_sign.setPlainText(data["signature"])
                
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Signed Successfully")  
                msg.exec_()
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print("Error:%s" % e)
    
    def call_api_verify(self):
        url = "http://127.0.0.1:5000/api/rsa/verify"  
        payload = {
            "message": self.ui.txt_info.toPlainText(),
            "signature": self.ui.txt_sign.toPlainText(),
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                if data["is_verified"]:  
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Verified Successfully")  
                    msg.exec_()
                else:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Verification Failed")  
                    msg.exec_()
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print("Error:%s" % e)
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
