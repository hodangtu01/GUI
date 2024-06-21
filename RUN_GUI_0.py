from PyQt5.QtCore import Qt, pyqtSignal, QObject
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtWidgets as QtGui
from docx import Document
from GUI_0 import Ui_MainWindow
from mqtt import MQTT


style = ["color: rgb(255, 255, 255);\n" + \
        "font: 700 15pt \"Times New Roman\";\n" + \
        "background-color: rgb(62, 91, 255);\n" + \
        "border-radius: 20px;\n",

        "color: rgb(255, 255, 255);\n" + \
                "font: 700 15pt \"Times New Roman\";\n" + \
                "background-color: rgb(47, 48, 206);\n" + \
                "border-radius: 20px;\n" + \
                "border-bottom: 5px solid black;\n"
        ]

IDLE = 0
ORDER = 1
DELIVER = 2
class Window(QMainWindow, Ui_MainWindow):
    message_received = pyqtSignal(str)  
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupUi(self)
        self.mqtt_client = None  # Initialize the mqtt_client as None


        self.Btn_Run_Ban_1.setStyleSheet(style[0])
        self.Btn_Run_Ban_2.setStyleSheet(style[0])
        self.Btn_Run_Ban_3.setStyleSheet(style[0])
        self.Btn_Run_Ban_4.setStyleSheet(style[0])
        self.Btn_Ra_Ban_1.setStyleSheet(style[0])
        self.Btn_Ra_Ban_2.setStyleSheet(style[0])
        self.Btn_Ra_Ban_3.setStyleSheet(style[0])
        self.Btn_Ra_Ban_4.setStyleSheet(style[0])

        self.mode = IDLE

    def on_message(self, client, userdata, message):
        print("Received message %s from client %s" % (message.payload, client._client_id))
        command = message.payload.decode("utf-8")
        self.message_received.emit(command)  # Emit the signal with the message

    def update_text_browser(self, message):
        self.txt_order_index_0.append(message)
    
    def connect_to_mqtt(self):
        if self.mqtt_client is None:
            self.mqtt_client = MQTT(client_id="hodangtu0601", broker="e94ecb09544d4cd39ee5231c33b0f001.s2.eu.hivemq.cloud", port=8883, keepalive=60)
            self.mqtt_client.set_credentials(username="hodangtu0601", password="Hodangtu!@3")
            self.mqtt_client.set_callback(on_connect=True, on_subscribe=True)
            self.mqtt_client.set_on_message_callback(self.on_message)
            self.message_received.connect(self.update_text_browser)
            self.mqtt_client.connect()
            self.mqtt_client.loop_start()
            # Subscribe to a topic
            self.mqtt_client.subscribe("client/bill")

    def disconnect_from_mqtt(self):
        if self.mqtt_client is not None:
            self.mqtt_client.disconnect()
            self.mqtt_client = None  # Reset the mqtt_client

    def changeMode(self, mode:int):
        if (self.mode != mode):

            if self.mode == DELIVER:
                if self.Btn_Ra_Ban_1.isChecked():
                    self.Btn_Ra_Ban_1.click()
                    self.Btn_Ra_Ban_1.setStyleSheet(style[0])

                if self.Btn_Ra_Ban_2.isChecked():
                    self.Btn_Ra_Ban_2.click()
                    self.Btn_Ra_Ban_2.setStyleSheet(style[0])

                if self.Btn_Ra_Ban_3.isChecked():
                    self.Btn_Ra_Ban_3.click()
                    self.Btn_Ra_Ban_3.setStyleSheet(style[0])

                if self.Btn_Ra_Ban_4.isChecked():
                    self.Btn_Ra_Ban_4.click()
                    self.Btn_Ra_Ban_4.setStyleSheet(style[0])

            elif self.mode == ORDER:
                if self.Btn_Run_Ban_1.isChecked():
                    self.Btn_Run_Ban_1.setChecked(False)
                    self.Btn_Run_Ban_1.setStyleSheet(style[0])

                if self.Btn_Run_Ban_2.isChecked():
                    self.Btn_Run_Ban_2.setChecked(False)
                    self.Btn_Run_Ban_2.setStyleSheet(style[0])

                if self.Btn_Run_Ban_3.isChecked():
                    self.Btn_Run_Ban_3.setChecked(False)
                    self.Btn_Run_Ban_3.setStyleSheet(style[0])

                if self.Btn_Run_Ban_4.isChecked():
                    self.Btn_Run_Ban_4.setChecked(False)
                    self.Btn_Run_Ban_4.setStyleSheet(style[0])

            self.mode = mode

        # CODE DIEU KHIEN DONG CO CHAY RA ORDER

    def slot_pub(self):
        cmd: str = ""
        if self.mode == ORDER:
            if self.Btn_Run_Ban_1.isChecked():
                cmd += "1-"
            if self.Btn_Run_Ban_2.isChecked():
                cmd += "2-"
            if self.Btn_Run_Ban_3.isChecked():
                cmd += "3-"
            if self.Btn_Run_Ban_4.isChecked():
                cmd += "4-"
        elif self.mode == DELIVER:
            if self.Btn_Ra_Ban_1.isChecked():
                cmd += "1/%d-" % (self.cbBox_Khay_index_1.currentIndex() + 1)
            if self.Btn_Ra_Ban_2.isChecked():
                cmd += "2/%d-" % (self.cbBox_Khay_index_2.currentIndex() + 1)
            if self.Btn_Ra_Ban_3.isChecked():
                cmd += "3/%d-" % (self.cbBox_Khay_index_3.currentIndex() + 1)
            if self.Btn_Ra_Ban_4.isChecked():
                cmd += "4/%d-" % (self.cbBox_Khay_index_4.currentIndex() + 1)
                
        if cmd == "":
            return

        if self.mode == ORDER:
            self.changeMode(DELIVER)

            self.mqtt_client.publish("manager/order", cmd)
        elif self.mode == DELIVER:
            self.changeMode(ORDER)

            self.mqtt_client.publish("manager/deliver", cmd)


    def slot1(self):

        self.changeMode(ORDER)

        sender = self.sender()
        match sender:
            case self.Btn_Run_Ban_1:
                self.Btn_Run_Ban_1.setStyleSheet(style[self.Btn_Run_Ban_1.isChecked()])
            case self.Btn_Run_Ban_2:
                self.Btn_Run_Ban_2.setStyleSheet(style[self.Btn_Run_Ban_2.isChecked()])
            case self.Btn_Run_Ban_3:
                self.Btn_Run_Ban_3.setStyleSheet(style[self.Btn_Run_Ban_3.isChecked()])
            case self.Btn_Run_Ban_4:
                self.Btn_Run_Ban_4.setStyleSheet(style[self.Btn_Run_Ban_4.isChecked()])

    def slot2(self):
        self.changeMode(DELIVER)
        sender = self.sender()
        match sender:
            case self.Btn_Ra_Ban_1:
                self.Btn_Ra_Ban_1.setStyleSheet(style[self.Btn_Ra_Ban_1.isChecked()])
            case self.Btn_Ra_Ban_2:
                self.Btn_Ra_Ban_2.setStyleSheet(style[self.Btn_Ra_Ban_2.isChecked()])
            case self.Btn_Ra_Ban_3:
                self.Btn_Ra_Ban_3.setStyleSheet(style[self.Btn_Ra_Ban_3.isChecked()])
            case self.Btn_Ra_Ban_4:
                self.Btn_Ra_Ban_4.setStyleSheet(style[self.Btn_Ra_Ban_4.isChecked()])

    
    def slot3(self):
        # CHUC NANG HIEN THI 'CONNECT - DISCONNECT' MQTT
        if self.Btn_Cnt_MQTT.isChecked():
            self.Btn_Cnt_MQTT.setText("KẾT NỐI")
            self.Btn_Cnt_MQTT.setStyleSheet(
                "QPushButton {\n"
                "color: rgb(250, 250, 250);\n"
                "font: 700 12pt \"Times New Roman\";\n"
                "border-radius: 20px;\n"";\n"
                "background-color: rgb(5, 208, 50);\n""}\n""\n"
                "QPushButton:pressed {\n""\n"
                "background-color: rgb(5,208, 50);\n"
                "color: rgb(250, 250, 250);\n"
                "font: 700 12pt \"Times New Roman\";\n"
                "border-bottom: 5px solid black;\n""}\n""")
            self.connect_to_mqtt()
        else:
            self.Btn_Cnt_MQTT.setText('NGẮT KẾT NỐI')
            self.Btn_Cnt_MQTT.setStyleSheet(
                "QPushButton {\n"
                "color: rgb(250, 250, 250);\n"
                "font: 700 12pt \"Times New Roman\";\n"
                "border-radius: 20px;\n"";\n"
                "background-color: rgb(118, 118, 118);\n""}\n""\n"
                "QPushButton:pressed {\n""\n"
                "background-color: rgb(118, 118, 118);\n"
                "color: rgb(250, 250, 250);\n"
                "font: 700 12pt \"Times New Roman\";\n"
                "border-bottom: 5px solid black;\n""}\n""")
            self.disconnect_from_mqtt()

    def slot4(self):
        text = self.txt_order_index_0.toPlainText()  # Get text from textBrowser
        if text:
            filename, _ = QtGui.QFileDialog.getSaveFileName(self, "Save Text", "", "*.docx")  # Open dialog to save the file
            if filename:
                try:
                    from docx import Document
                    document = Document()
                    document.add_paragraph(text)  # Add text to the document
                    document.save(filename)  # Save the document
                    print(f"Text saved to Word document: {filename}")
                except ImportError:
                    print("Error: docx library not installed. Please install using 'pip install docx'.")
                except Exception as e:
                    print(f"Error saving text: {e}")
            else:
                print("There's no text to save")

if __name__ == '__main__':
    app = QApplication([])
    window = Window()
    window.show()
    app.exec_()