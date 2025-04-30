import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.ecc import Ui_MainWindow
import requests

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.btn_gen_key.clicked.connect(self.call_api_gen_keys)
        self.ui.btn_sign.clicked.connect(self.call_api_sign)
        self.ui.btn_verify.clicked.connect(self.call_api_verify)
        
    def call_api_gen_keys(self):
        try:
            response = requests.get('http://localhost:5000/api/ecc/generate_keys')
            if response.status_code == 200:
                data = response.json()
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText(data["message"])
                msg.exec_()
            else:
                print("Error")
        except requests.exceptions.RequestException as e:
            print("Error: %s" % e)
            
    def call_api_sign(self):
        try:
            payload = {
                'message': self.ui.txt_info.toPlainText(),
            }
            response = requests.post('http://localhost:5000/api/ecc/sign', json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_sign.setPlainText(data["signature"])
                
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Signed Successfully")
                msg.exec_()
            else:
                print("Error")
        except requests.exceptions.RequestException as e:
            print("Error: %s" % e)
            
    def call_api_verify(self):
        try:
            payload = {
                'message': self.ui.txt_info.toPlainText(),
                'signature': self.ui.txt_sign.toPlainText(),
            }
            response = requests.post('http://localhost:5000/api/ecc/verify', json=payload)
            if response.status_code == 200:
                data = response.json()
                if (data["is_verified"]):
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("verified Successfully")
                    msg.exec_()
                else:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("verified fail")
                    msg.exec_()
            else:
                print("Error")
        except requests.exceptions.RequestException as e:
            print("Error: %s" % e)
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
        