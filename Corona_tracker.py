from PyQt5.QtWidgets import QMainWindow,QApplication,QWidget,QGridLayout,QVBoxLayout,QHBoxLayout,QLabel
from PyQt5.QtCore import Qt,QThread,pyqtSignal
import time
import requests
import sys

class MyThread(QThread):
    change_value=pyqtSignal()
    def run(self):
        while True:
            time.sleep(5)
            self.change_value.emit()




class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet('''
            *{
                background-color:black;
            }
            QWidget#state_widget{
                border:2px solid grey;
            }
            QLabel#state_name{
                color:white;
            }
        ''')
        self.setWindowTitle("CC Hacks")
        self.setGeometry(0,0,1920,1080)

        self.update()
        self.thread=MyThread()
        self.thread.change_value.connect(self.update)
        self.thread.start()
    
    def closeEvent(self,event):
        self.thread.terminate()

    
    def update(self):
        print('in')
        main_widget=QWidget()
        grid=QGridLayout()
        row=0
        column=0

        url='https://api.covid19india.org/data.json'
        req=requests.get(url)
        data=req.json()
        data=data['statewise']

        for i in range(len(data)):

            wid=QWidget()
            wid.setObjectName("state_widget")
            
            vbox=QVBoxLayout()

            if len(data[i]['state'])<=14:
                l=QLabel("<h1>"+data[i]['state']+"</h1>")
            elif len(data[i]['state'])<=17:
                l=QLabel("<h2>"+data[i]['state']+"</h2>")
            else:
                l=QLabel("<h4>"+data[i]['state']+"</h4>")
            l.setObjectName("state_name")
            l.setAlignment(Qt.AlignCenter)
            vbox.addWidget(l)

            hb=QHBoxLayout()
            hb.setContentsMargins(0,0,0,0)

            l22=QLabel("<h3 style='color:blue'>Total</h3>")
            l33=QLabel("<h3 style='color:green'>Recovered</h3>")
            l44=QLabel("<h3 style='color:red'>Deaths</h3>")
            l22.setAlignment(Qt.AlignCenter)
            l33.setAlignment(Qt.AlignCenter)
            l44.setAlignment(Qt.AlignCenter)

            hb.addWidget(l22)
            hb.addWidget(l33)
            hb.addWidget(l44)

            vbox.addLayout(hb)

            hbox=QHBoxLayout()

            h1=QVBoxLayout()
            l2=QLabel("<h3 style='color:blue'>"+data[i]['confirmed']+"</h3>")
            l2.setAlignment(Qt.AlignCenter)
            ll2=QLabel("<h3 style='color:blue'>"+data[i]['deltaconfirmed']+"</h3>")
            ll2.setAlignment(Qt.AlignCenter)
            h1.addWidget(l2)
            h1.addWidget(ll2)

            h2=QVBoxLayout()
            l3=QLabel("<h3 style='color:green'>"+data[i]['recovered']+"</h3>")
            l3.setAlignment(Qt.AlignCenter)
            ll3=QLabel("<h3 style='color:green'>"+data[i]['deltarecovered']+"</h3>")
            ll3.setAlignment(Qt.AlignCenter)
            h2.addWidget(l3)
            h2.addWidget(ll3)

            h3=QVBoxLayout()
            l4=QLabel("<h3 style='color:red'>"+data[i]['deaths']+"</h3>")
            l4.setAlignment(Qt.AlignCenter)
            ll4=QLabel("<h3 style='color:red'>"+data[i]['deltadeaths']+"</h3>")
            ll4.setAlignment(Qt.AlignCenter)
            h3.addWidget(l4)
            h3.addWidget(ll4)

            hbox.addLayout(h1)
            hbox.addLayout(h2)
            hbox.addLayout(h3)

            vbox.addLayout(hbox)


            wid.setLayout(vbox)

            if column==8:
                row+=1
                column=0
            grid.addWidget(wid,row,column)
            column+=1

            tm=QLabel("Last Updated")
            tm.setObjectName("state_name")
            tm.setAlignment(Qt.AlignCenter)
            tm2=QLabel(str(data[i]['lastupdatedtime']))
            tm2.setObjectName('state_name')
            tm2.setAlignment(Qt.AlignCenter)
            vbox.addWidget(tm)
            vbox.addWidget(tm2)

        
        grid.setSpacing(0)
        grid.setContentsMargins(0,0,0,0)
        main_widget.setLayout(grid)
        self.setCentralWidget(main_widget)






app=QApplication(sys.argv)
win=Window()
win.show()
app.exec_()