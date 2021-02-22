import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FC
from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow, QVBoxLayout, QWidget,QHBoxLayout
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class QtDraw(QWidget):
    def __init__(self,circus_df): #circus_df
        super(QtDraw, self).__init__()
        self.circus_df = circus_df
        self.resize(800, 550)
        self.fig = plt.Figure(tight_layout=True)
        self.canvas = FC(self.fig)

        self.setWindowTitle('circus')
        self.tools_layout = QHBoxLayout()

        self.btn_start = QPushButton('draw')
        self.down_botton = QPushButton('download')

        self.tools_layout.addWidget(self.btn_start)
        self.tools_layout.addWidget(self.down_botton)
        self.btn_start.clicked.connect(self.circus)
        self.down_botton.clicked.connect(self.download)      
        self.draw_layout  = QVBoxLayout()
        self.draw_layout.addWidget(self.canvas)

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.draw_layout)
        self.layout.addLayout(self.tools_layout)
        self.setLayout(self.layout)
  
    
    def circus(self):
        chrom_length = [43270824,35937251,36413820,35502336,29958035,31248788,29697618,28443023,23012618,23206949,29020344,27531654]
        #对变异类型进行区分
        circus_df = self.circus_df[['CHROM', 'POS', 'REF', 'ALT']]
        circus_df = circus_df.dropna()
        circus_df = circus_df.replace(['chr01','chr02','chr03','chr04','chr05','chr06','chr07','chr08','chr09','chr10','chr11','chr12'],[1,2,3,4,5,6,7,8,9,10,11,12])
        circus_df['POS'] = circus_df['POS'].astype('str').astype('int')
        circus_df['CHROM'] = circus_df['CHROM'].astype('str').astype('int')
        circus_df = circus_df.replace('./.','0/0')
        circus_df = circus_df.replace('.', 0)
        circus_df = circus_df.dropna()

        def get_type(ref,alt):
            if len(ref) == 1 and len(alt)==1:
                type = 'snp'
            else:
                type = 'indel'
            return type
        circus_df['type']=circus_df.apply(lambda x: get_type(x.REF,x.ALT), axis = 1)
        #接下来是进行滑窗，会生成一个新的circus_df
        chorms_max = circus_df.groupby('CHROM')['POS'].max()
        circus_df_window = pd.DataFrame()
        for i in range(1,13):
            max = chorms_max[i]
            window_start = 0
            while window_start < max:
                circus_df_window = circus_df_window.append({'chrom':int(i),'window_start':window_start},ignore_index=True)
                window_start = window_start+100*1000
            circus_df_window.eval('window_end = window_start+100*1000',inplace=True)
            circus_df_window.eval('window_central = window_start+50*1000',inplace=True)

        #计算每个窗口内snp和indel的数量
        def snp_count(chrom,window_start,window_end,circus_df):
            snp_count= ''
            data_circus_df = circus_df[circus_df['CHROM'] == chrom]
            data_circus_df = data_circus_df[(data_circus_df['POS']<window_end) & (data_circus_df['POS']> window_start)]
            data_circus_df = data_circus_df[data_circus_df['type'] == 'snp']
            snp_count = data_circus_df.shape[0]
            if snp_count != 0:
                snp_count = snp_count/1500
            return snp_count
        def indel_count(chrom,window_start,window_end,circus_df):
            indel_count= ''
            data_circus_df = circus_df[circus_df['CHROM'] == chrom]
            data_circus_df = data_circus_df[(data_circus_df['POS']<window_end) & (data_circus_df['POS']> window_start)]
            data_circus_df = data_circus_df[data_circus_df['type'] == 'indel']
            indel_count = data_circus_df.shape[0]
            if indel_count != 0:
                indel_count = indel_count/1500
            return indel_count
        circus_df_window['snp_count']=circus_df_window.apply(lambda x: snp_count(x.chrom,x.window_start,x.window_end,circus_df),axis = 1)
        circus_df_window['indel_count']=circus_df_window.apply(lambda x: indel_count(x.chrom,x.window_start,x.window_end,circus_df),axis = 1)
        
        rows = circus_df_window.shape[0]
        #开始绘图
        plt.style.use('ggplot')
        ax = self.fig.add_subplot(111,projection='polar')
        #设置为顺时针
        ax.set_theta_direction(-1)
        #正上方为0度
        ax.set_theta_zero_location('N')
        #绘制柱状图，角度对应位置，半径对应高度
        #先画最外面一圈,留下约15度的缺口，写图标，然后每个染色体中间空一格
        i = 0
        sum = 0
        left = []
        while i < 12:
            left.append(sum)
            sum += chrom_length[i]
            i += 1
        n = 0
        new_left = []
        while n < 12:
            ax.barh(height=0.2,width=(2-(1/12)-(1/36))*np.pi*chrom_length[n]/sum,y=4,left = np.pi/12+(2-(1/12)-(1/36))*np.pi*left[n]/sum+np.pi/360*n)
            new_left.append(np.pi/12+(2-(1/12)-(1/36))*np.pi*left[n]/sum+np.pi/360*n)
            n += 1
        #位置，高度，宽度,离圆心的距离
        j = 0
        while j < 12:
            data_circus_df = circus_df_window[circus_df_window['chrom'] == j+1]
            ax.bar(np.linspace(new_left[j],new_left[j]+(2-(1/12)-(1/36))*np.pi*data_circus_df.shape[0]/rows,data_circus_df.shape[0]),data_circus_df['snp_count'],width=(2-(1/12)-(1/36))*np.pi/rows,bottom = 2.5,color='green')
            ax.bar(np.linspace(new_left[j],new_left[j]+(2-(1/12)-(1/36))*np.pi*data_circus_df.shape[0]/rows,data_circus_df.shape[0]),data_circus_df['indel_count'],width=(2-(1/12)-(1/36))*np.pi/rows,bottom = 1.5,color='orange')
            j = j+1
        ax.text(np.pi/24,4,'A')
        ax.text(np.pi/24,3,'B')
        ax.text(np.pi/24,2,'C')
        ax.axis('off')
        self.canvas.draw()
    def download(self):
        filename = QFileDialog.getSaveFileName(self,'save file','','Image files(*.jpg *.gif *.png)')
        with open(filename[0],'w') as f:
            self.fig.savefig(filename[0],dpi=600)
 