import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from mutmap_page import MutmapPage
from BSR_page import BSRPage
from Qtlseq_page import QtlPqge
from fisher_page import fisher_page
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
        self.setWindowTitle('IBSA')
        self.welcome_label= QLabel('欢迎使用IBSA')

        self.upload_button = QPushButton('上传文件')
        self.upload_button.clicked.connect(self.uploausr_dfile)
        self.contents = QTextBrowser()
        self.mutmap_button = QPushButton('mutmap')
        self.mutmap_button.clicked.connect(self.open_mutmap_page)
        self.qtl_button = QPushButton('qtl-seq')
        self.qtl_button.clicked.connect(self.open_qtl_page)
        self.bsr_button = QPushButton('bsr')
        self.bsr_button.clicked.connect(self.open_bsr_page)
        self.circle_button = QPushButton('circus')
        self.circle_button.clicked.connect(self.open_circus_page)
        self.fisher_button = QPushButton('fisher')
        self.fisher_button.clicked.connect(self.open_fisher_page)
        
        self.ways_layout = QGridLayout()
        self.upload_layout = QVBoxLayout()
        self.all_layout = QVBoxLayout()
        self.upload_layout.addWidget(self.welcome_label)

        self.upload_layout.addWidget(self.upload_button)
        self.upload_layout.addWidget(self.contents)
        self.ways_layout.addWidget(self.mutmap_button, 0, 0)
        self.ways_layout.addWidget(self.bsr_button, 0, 1)
        self.ways_layout.addWidget(self.qtl_button, 1, 0)
        self.ways_layout.addWidget(self.circle_button, 1, 1)
        self.ways_layout.addWidget(self.fisher_button, 2, 0)

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
        self.mutmap_page = MutmapPage(self.usr_df,self.usr_df_index,self.mode)
        self.mutmap_page.show()
        self.close()
    def open_qtl_page(self):
        self.qtl_page = QtlPqge(self.usr_df,self.usr_df_index)
        self.qtl_page.show()
        self.close()
    def open_bsr_page(self):
        self.bsr_page = BSRPage(self.usr_df,self.usr_df_index)
        self.bsr_page.show()
        self.close()
    def open_circus_page(self):
        self.circus_page = QtDraw(self.usr_df)
        self.circus_page.show()
        self.close()
    def open_fisher_page(self):
        self.fisher_page = fisher_page(self.usr_df,self.usr_df_index)
        self.fisher_page.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv) 
    Imut_first_page = FirstPage()
    Imut_first_page.show()
    sys.exit(app.exec_())


