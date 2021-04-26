import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from mutmap_page import MutmapPage
from MM_page import MMPage
from Qtlseq_page import QtlPqge
from fisher_page import fisher_page
from Gps_page import GpsPage
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
from qtdraw import QtDraw
import scipy.special.cython_special
from scipy import stats
import math

class FirstPage(QWidget):

    def __init__(self):
        super(FirstPage,self).__init__()
        self.setWindowTitle('IBSA V1.0.2')
        self.welcome_label= QLabel('Welcome to use IBSA!'+'\n'+'Feel free to conact us!')

        self.upload_button = QPushButton('Upload')
        self.upload_button.clicked.connect(self.uploausr_dfile)
        self.contents = QTextBrowser()
        self.mutmap_button = QPushButton('Mutmap')
        self.mutmap_button.clicked.connect(self.open_mutmap_page)
        self.qtl_button = QPushButton('QTL-seq')
        self.qtl_button.clicked.connect(self.open_qtl_page)
        self.mm_button = QPushButton('Modified MutMap')
        self.mm_button.clicked.connect(self.open_mm_page)
        self.circle_button = QPushButton('Circus')
        self.circle_button.clicked.connect(self.open_circus_page)
        self.fisher_button = QPushButton('Fisher')
        self.fisher_button.clicked.connect(self.open_fisher_page)
        self.GPS_button = QPushButton('GradedPool-Seq')
        self.GPS_button.clicked.connect(self.open_GPS_page)

        self.ways_layout = QGridLayout()
        
        self.upload_layout = QVBoxLayout()
        self.all_layout = QVBoxLayout()
        self.upload_layout.addWidget(self.welcome_label)

        self.upload_layout.addWidget(self.upload_button)
        self.upload_layout.addWidget(self.contents)
        self.ways_layout.addWidget(self.mutmap_button, 0, 0)
        self.ways_layout.addWidget(self.mm_button, 0, 1)
        self.ways_layout.addWidget(self.qtl_button, 1, 0)
        self.ways_layout.addWidget(self.circle_button, 1, 1)
        self.ways_layout.addWidget(self.fisher_button, 2, 0)
        self.ways_layout.addWidget(self.GPS_button, 2, 1)

        self.all_layout.addLayout(self.upload_layout)
        self.all_layout.addLayout(self.ways_layout)
        self.setLayout(self.all_layout)
        self.resize(800,550)

    def uploausr_dfile(self):
        usr_df = pd.DataFrame()
        i = 0
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        if dlg.exec_():
            filename = dlg.selectedFiles()
            f = open(filename[0], 'r')
            with f:
               lines = f.read().split('\n')
            #找到header
            for line in lines:
                if re.match("##", line, flags=0):
                    i = i +1
                else:
                    break
            usr_df = pd.DataFrame(lines[i+1:])
            usr_df = usr_df[0].str.split('\t', expand=True)
            usr_df_index = lines[i][1:].split('\t')
            usr_df.columns=usr_df_index
            self.contents.setText(str(usr_df.iloc[1:2]))
            self.usr_df =usr_df
            self.usr_df_index = usr_df_index
    
                  
    def open_mutmap_page(self):
        self.mutmap_page = MutmapPage(self.usr_df,self.usr_df_index)
        self.mutmap_page.show()
        
    def open_qtl_page(self):
        self.qtl_page = QtlPqge(self.usr_df,self.usr_df_index)
        self.qtl_page.show()
        
    def open_mm_page(self):
        self.mm_page = MMPage(self.usr_df,self.usr_df_index)
        self.mm_page.show()

    def open_circus_page(self):
        self.circus_page = QtDraw(self.usr_df)
        self.circus_page.show()
        
    def open_fisher_page(self):
        self.fisher_page = fisher_page(self.usr_df,self.usr_df_index)
        self.fisher_page.show()
        
    def open_GPS_page(self):
        self.GPS_page = GpsPage(self.usr_df,self.usr_df_index)
        self.GPS_page.show()

if __name__ == "__main__":
    app = QApplication(sys.argv) 
    Imut_first_page = FirstPage()
    Imut_first_page.show()
    sys.exit(app.exec_())


