from pynput import mouse #https://pypi.org/project/pynput/
import pyscreenshot as ImageGrab #https://github.com/ponty/pyscreenshot/tree/3.1
import sys
from PySide6 import QtCore, QtWidgets, QtGui
import time, os


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Screenshoter")
        self.await_release = False
        self.setFixedSize(500,500)
        self.positions = [None, None, None, None]  # Default positions (x1, y1, x2, y2)
        
        self.nr = 0

        self.tb_speicherort = QtWidgets.QLineEdit(sys.path[0])
        self.preview_label = QtWidgets.QLabel("Noch kein Screenshot geladen", alignment=QtCore.Qt.AlignCenter)
        self.preview_label.setMinimumHeight(240)
        self.preview_label.setStyleSheet("QLabel { border: 1px solid #888; background: #111; color: #ddd; }")

        self.tb_x1 = QtWidgets.QLineEdit(str(self.positions[0]))
        self.tb_y1 = QtWidgets.QLineEdit(str(self.positions[1]))
        self.tb_x2 = QtWidgets.QLineEdit(str(self.positions[2]))
        self.tb_y2 = QtWidgets.QLineEdit(str(self.positions[3]))

        self.get_initial_positions()
        
    

        self.tb_name = QtWidgets.QLineEdit("Bild")
        

        self.button_screenshot = QtWidgets.QPushButton("Screenshot")
        self.layout = QtWidgets.QVBoxLayout(self)
        newlayout = QtWidgets.QHBoxLayout()
        newlayout.addWidget(QtWidgets.QLabel("Name:"))
        newlayout.addWidget(self.tb_name)
        self.layout.addLayout(newlayout)

        newlayout = QtWidgets.QHBoxLayout()
        newlayout.addWidget(QtWidgets.QLabel("Pfad:"))
        newlayout.addWidget(self.tb_speicherort)
        self.layout.addLayout(newlayout)
        self.layout.addWidget(self.button_screenshot)
        self.layout.addWidget(self.preview_label)
        


        newlayout =QtWidgets.QHBoxLayout()
        newlayout.addWidget(QtWidgets.QLabel("X1:"))
        newlayout.addWidget(self.tb_x1)
        newlayout.addWidget(QtWidgets.QLabel("Y1:"))
        newlayout.addWidget(self.tb_y1)       
        newlayout.addWidget(QtWidgets.QLabel("X2:"))
        newlayout.addWidget(self.tb_x2)
        newlayout.addWidget(QtWidgets.QLabel("Y2:"))
        newlayout.addWidget(self.tb_y2) 
        self.layout.addLayout(newlayout)

        self.button_update_positions = QtWidgets.QPushButton("Update Positions")
        self.button_update_positions.clicked.connect(self.update_positions)
        self.button_new_positions = QtWidgets.QPushButton("catch new Position")
        self.button_new_positions.clicked.connect(self.get_initial_positions)
        newlayout =QtWidgets.QHBoxLayout()
        newlayout.addWidget(self.button_new_positions)
        newlayout.addWidget(self.button_update_positions)
        self.layout.addLayout(newlayout)


        self.button_screenshot.clicked.connect(self.screenshot)
        self.load_last_screenshot()

    def screenshot(self):
        # grab a specific area
        im = ImageGrab.grab(bbox=self.positions)
        nr = 0
        
        name = self.tb_name.text() +".png"

        while  os.path.exists(self.tb_speicherort.text() +"\\" + name):
            nr += 1
            #print(name)
            name = self.tb_name.text() +"_"+ str(nr) + ".png"
            
        # save image file
        
        im.save(self.tb_speicherort.text() +"\\" + name)
        self.nr += 1
        self.load_last_screenshot()

    def load_last_screenshot(self):
        folder = self.tb_speicherort.text().strip() or r"C:\Users\Johannes\Desktop\Screenshots"
        if not os.path.isdir(folder):
            self.preview_label.setText("Ungültiger Speicherort")
            self.preview_label.setPixmap(QtGui.QPixmap())
            return

        candidates = [
            os.path.join(folder, file_name)
            for file_name in os.listdir(folder)
            if file_name.lower().endswith(".png")
        ]
        if not candidates:
            self.preview_label.setText("Noch kein Screenshot gefunden")
            self.preview_label.setPixmap(QtGui.QPixmap())
            return

        latest_file = max(candidates, key=os.path.getmtime)
        pixmap = QtGui.QPixmap(latest_file)
        if pixmap.isNull():
            self.preview_label.setText("Screenshot konnte nicht geladen werden")
            self.preview_label.setPixmap(QtGui.QPixmap())
            return

        scaled = pixmap.scaled(
            self.preview_label.size(),
            QtCore.Qt.KeepAspectRatio,
            QtCore.Qt.SmoothTransformation,
        )
        self.preview_label.setPixmap(scaled)
        self.preview_label.setText("")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if not self.preview_label.pixmap().isNull():
            self.load_last_screenshot()

    def update_positions(self):
        try:
            self.positions = [int(self.tb_x1.text()),
                              int(self.tb_y1.text()),
                              int(self.tb_x2.text()),
                              int(self.tb_y2.text())]
        except ValueError:
            print("Invalid position values. Please enter valid integers.")
    
    def get_initial_positions(self):
        print('Click on the first position')
        
        self.positions = [None, None, None, None]

        listener = mouse.Listener(on_click=self.on_click)
        listener.start()
        while self.positions[0] is None:
            time.sleep(0.1)
        listener.stop()
        
        
        listener = mouse.Listener(on_click=self.on_click)
        listener.start()
        print('Click on the second position')
        while self.positions[2] is None and self.positions[0]!= self.positions[2]:
            time.sleep(0.5)

        listener.stop()
        self.await_release = False
        
        self.tb_x1.setText(str(self.positions[0]))
        self.tb_y1.setText(str(self.positions[1]))
        self.tb_x2.setText(str(self.positions[2]))
        self.tb_y2.setText(str(self.positions[3]))
        return self.positions
        
    
    def on_click(self, x, y, button, pressed):
        if self.await_release == True:
            self.await_release = False
            return True
        if pressed and self.positions[0] is None:
            self.positions[0] = x
            self.positions[1] = y
            self.await_release = True
            print("p1 = ", (x, y))
            time.sleep(0.5)
            return True
        if pressed and self.positions[2] is None:
            self.positions[2] = x
            self.positions[3] = y
            print("p2 = ", (x, y))
            return False
        


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    print(os.path.dirname(os.path.abspath(sys.argv[0])))

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())