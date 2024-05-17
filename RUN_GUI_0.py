from PyQt5.QtGui import QKeyEvent
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QMainWindow)

from GUI_0 import Ui_MainWindow

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupUi(self)

    def slot1(self):
        # Sau khi nhan RUN thi trang thai cac nut tro ve lai
        ButtonPressed = self.sender()
        if ButtonPressed == self.Btn_Run:
            self.Btn_Run_Ban_1.setChecked(False)
            self.Btn_Run_Ban_2.setChecked(False)
            self.Btn_Run_Ban_3.setChecked(False)
            self.Btn_Run_Ban_4.setChecked(False)   

        # CODE DIEU KHIEN DONG CO CHAY RA ORDER

    def slot2(self):
        pass
        # CODE DIEU KHIEN DONG CO CHAY RA DUA DO
    

    def slot3(self):
        # CHUC NANG HIEN THI 'CONNECT - DISCONNECT' MQTT
        ButtonPressed = self.sender()
        if ButtonPressed == self.Btn_Cnt_MQTT:
            if self.Btn_Cnt_MQTT.isChecked():
                self.Btn_Cnt_MQTT.setText('CONNECT')
            if not self.Btn_Cnt_MQTT.isChecked():
                self.Btn_Cnt_MQTT.setText('DISCONNECT')

        # HAM KET NOI MQTT
        

    
if __name__ == '__main__':
    app = QApplication([])
    window = Window()
    window.show()
    app.exec_()