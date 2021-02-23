import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FC
from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow, QVBoxLayout, QWidget,QHBoxLayout
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from scipy import stats
import scipy.special.cython_special
import math


class fisher_page(QTabWidget):
    def __init__(self,fisher_df,fisher_df_index):
        super(fisher_page,self).__init__()
        self.resize(800,550)
        self.setWindowTitle('fisher')
        plt.style.use('ggplot')
        self.fig = plt.Figure()
        self.canvas = FC(self.fig)
        self.tab1=QWidget()
        self.tab2=QWidget()
        self.fisher_df = fisher_df
        self.fisher_df_index = fisher_df_index
        self.addTab(self.tab1, 'info')
        self.addTab(self.tab2, 'fisher_exact')
        self.tab1UI()
        self.tab2UI()


    def tab1UI(self):
        pool_1_label = QLabel('pool_1')
        self.pool_1_combox = QComboBox()
        self.pool_1_combox.addItems(self.fisher_df_index)
        self.pool_1_combox.currentIndexChanged.connect(self.selectpool_1)

        pool_2_label = QLabel('pool_2')
        self.pool_2_combox = QComboBox()
        self.pool_2_combox.addItems(self.fisher_df_index)
        self.pool_2_combox.currentIndexChanged.connect(self.selectpool_2)

        next_step_button_1 = QPushButton('next')
        next_step_button_1.clicked.connect(self.clean_df)
        next_step_button_2 = QPushButton('next')
        next_step_button_2.clicked.connect(self.slide_window)

        min_depth_label = QLabel('min_depth')
        self.min_depth_spinbox = QSpinBox()
        self.min_depth_spinbox.setMinimum(0)
        self.min_depth_spinbox.setMaximum(15)
        self.min_depth_spinbox.setValue(5)
        max_depth_label = QLabel('max_depth')
        self.max_depth_spinbox = QSpinBox()
        self.max_depth_spinbox.setMinimum(200)
        self.max_depth_spinbox.setMaximum(500)
        self.max_depth_spinbox.setValue(300)
        win_size_label = QLabel('window_size')
        self.win_size_spinbox = QSpinBox()
        self.win_size_spinbox.setMinimum(0)
        self.win_size_spinbox.setMaximum(50000)
        self.win_size_spinbox.setValue(2000)
        win_step_label = QLabel('window_step')
        self.win_step_spinbox = QSpinBox()
        self.win_step_spinbox.setMinimum(0)
        self.win_step_spinbox.setMaximum(10000)
        self.win_step_spinbox.setValue(100)
        n_snp_label = QLabel('n_snp_in_window')
        self.n_snp_spinbox = QSpinBox()
        self.n_snp_spinbox.setMinimum(0)
        self.n_snp_spinbox.setMaximum(20)
        self.n_snp_spinbox.setValue(0)
        layout = QGridLayout()
        layout.addWidget(pool_1_label, 0, 0)
        layout.addWidget(self.pool_1_combox,0, 1)
        layout.addWidget(pool_2_label, 1, 0)
        layout.addWidget(self.pool_2_combox, 1, 1)
        layout.addWidget(min_depth_label,2,0)
        layout.addWidget(self.min_depth_spinbox,2,1)
        layout.addWidget(max_depth_label,3,0)
        layout.addWidget(self.max_depth_spinbox,3,1)
        layout.addWidget(next_step_button_1, 5, 1)
        layout.addWidget(win_size_label,6,0)
        layout.addWidget(self.win_size_spinbox,6,1)
        layout.addWidget(win_step_label,7,0)
        layout.addWidget(self.win_step_spinbox,7,1)
        layout.addWidget(n_snp_label,8,0)
        layout.addWidget(self.n_snp_spinbox,8,1)
        layout.addWidget(next_step_button_2,9,1)
        self.tab1.setLayout(layout)
    
    def tab2UI(self):

        tools_layout = QHBoxLayout()

        btn_start = QPushButton('draw')
        btn_start.clicked.connect(self.draw)
        down_botton_1 = QPushButton('download_picture')
        down_botton_2 = QPushButton('download_window')
        down_botton_3 = QPushButton('download_variant')
        tools_layout.addWidget(btn_start)
        tools_layout.addWidget(down_botton_1)
        tools_layout.addWidget(down_botton_2)
        tools_layout.addWidget(down_botton_3)

   
        draw_layout  = QVBoxLayout()
        draw_layout.addWidget(self.canvas)

        layout = QVBoxLayout()
        layout.addLayout(draw_layout)
        layout.addLayout(tools_layout)
        self.tab2.setLayout(layout)
        down_botton_1.clicked.connect(self.download_picture)  
        down_botton_2.clicked.connect(self.download_window)
        down_botton_3.clicked.connect(self.download_variant)   

    def selectpool_2(self):
        self.pool_2_index = self.pool_2_combox.currentIndex()
    
    def selectpool_1(self):
        self.pool_1_index = self.pool_1_combox.currentIndex()
    
    
    def clean_df(self):
        df = self.fisher_df
        min_depth = self.min_depth_spinbox.value()
        max_depth = self.max_depth_spinbox.value()
        filed_index=[]
        filed = df.loc[0,'FORMAT'].split(':')
        filed_index.append(filed.index('GT'))
        filed_index.append(filed.index('AD'))
        if 'DP' in filed:
            filed_index.append(filed.index('DP'))
        pool_1 = df.iloc[:,self.pool_1_index].str.split(':', expand=True).iloc[:,filed_index]
        pool_1.columns = ['pool_1_gt', 'pool_1_ad','pool_1_dp']
        pool_2 = df.iloc[:,self.pool_2_index].str.split(':', expand=True).iloc[:, filed_index]
        pool_2.columns = ['pool_2_gt', 'pool_2_ad','pool_2_dp']
        df = pd.concat([df,pool_1,pool_2], axis= 1)
        #对一些需要的部分进行过滤
        df.dropna(inplace=True)
        df = df.replace(['.|.', '0|0','0|1','1|1','0|2','1|2','2|2'],['./.', '0/0','0/1','1/1','0/2','1/2','2/2'])
        df = df.replace('./.','0/0')
        df = df.replace('.', 0)
        df['pool_1_dp'] = df['pool_1_dp'].astype('str').astype('int')
        df['pool_2_dp'] = df['pool_2_dp'].astype('str').astype('int')
        df['POS'] = df['POS'].astype('str').astype('int')
        df = df[df['pool_1_dp']>min_depth]
        df = df[df['pool_1_dp']<max_depth]
        df = df[df['pool_2_dp']>min_depth]
        df = df[df['pool_2_dp']<max_depth]
        df.dropna(inplace=True)
        self.chroms = df['CHROM'].unique()
        self.chrom_count =len(self.chroms)
        df['bulk1_ref'] = df['pool_1_ad'].str.split(',').str[0]
        df['bulk1_alt'] = df['pool_1_ad'].str.split(',').str[1]
        df['bulk2_ref'] = df['pool_2_ad'].str.split(',').str[0]
        df['bulk2_alt'] = df['pool_2_ad'].str.split(',').str[1]
        df[['k','pvalue']]= df.apply(lambda x:stats.fisher_exact([[x.bulk1_alt,x.bulk1_ref],[x.bulk2_alt,x.bulk2_ref]], alternative='two-sided'),axis = 1,result_type="expand")
        df['d']=df.apply(lambda x:-math.log(x.pvalue,10),axis = 1)
        df['POS']=df['POS'].astype('str').astype('int')
        self.df = df[['CHROM', 'POS', 'REF', 'ALT','pool_1_gt','pool_2_gt','k','pvalue','d']]

    def slide_window(self):
        df = self.df
        win_size = self.win_size_spinbox.value()*1000
        win_step = self.win_step_spinbox.value()*1000
        chorms_max = df.groupby('CHROM')['POS'].max()
        df_window = pd.DataFrame()
        for i in range(0,self.chrom_count):
            max = chorms_max[i]
            window_end = win_size
            while window_end < max:
                df_window = df_window.append({'chrom':self.chroms[i],'window_end':window_end,'window_start':window_end-win_size},ignore_index=True)
                window_end = window_end+win_step
        df_window.eval('window_central = (window_start+window_end)/2',inplace=True)
        def get_slide_index(chrom,window_start,window_end,df):
            n_snp = self.n_snp_spinbox.value()
            data_df = df[df['CHROM'] == chrom]
            data_df = data_df[(data_df['POS']<window_end) & (data_df['POS']> window_start)]
            if data_df.shape[0] > n_snp:
                slide_index = data_df['d'].mean()
            else:
                slide_index =None
            return slide_index
        df_window['slide_pvalue']=df_window.apply(lambda x: get_slide_index(x.chrom,x.window_start,x.window_end,df),axis = 1)
        self.df_window = df_window

    def draw(self):
        if self.chrom_count % 2 == 0:
            pic_row=self.chrom_count/2
        else:
            pic_row = (self.chrom_count+1)/2

        for i in range(0,self.chrom_count):
            draw_df_1 = self.df_window[self.df_window['chrom'] == self.chroms[i]]
            draw_df_2 = self.df[self.df['CHROM'] == self.chroms[i]]
            ax = self.fig.add_subplot(2,pic_row,i+1)
            ax.cla()
            ax.plot(draw_df_1['window_central']/1000000,draw_df_1['slide_pvalue'],c='red',linewidth=3)
            ax.axhline(y=-math.log(0.01,10), c="g", ls="--")
            ax.scatter(draw_df_2['POS']/1000000,draw_df_2['d'],c='blue',alpha=0.4)
            ax.set_title(self.chroms[i])
            ax.set_xlabel('position (Mb)')
            ax.set_ylabel('-log10(pvalue)')
            ax.set_ylim(0, 10.1)
        self.fig.subplots_adjust(wspace=0.5, hspace=0.3)
        self.canvas.draw()
    def download_picture(self):
        filename = QFileDialog.getSaveFileName(self,'save file','','Image files(*.jpg *.gif *.png)')
        with open(filename[0],'w') as f:
            self.fig.savefig(filename[0],dpi=600)
    def download_window(self):
            filename = QFileDialog.getSaveFileName(self,'save file','','Text Files (*.txt)')
            with open(filename[0],'w') as f:
                self.df_window.to_csv(filename[0],sep='\t',index=False)
    def download_variant(self):
            filename = QFileDialog.getSaveFileName(self,'save file','','Text Files (*.txt)')
            with open(filename[0],'w') as f:
                self.df.to_csv(filename[0],sep='\t',index=False)