import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FC
from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow, QVBoxLayout, QWidget,QHBoxLayout
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *



class QtlPqge(QTabWidget):
    def __init__(self,BSR_df,BSR_df_index):
        super(QtlPqge,self).__init__()
        self.resize(800,550)
        self.setWindowTitle('qtl_seq')
        self.fig_1 = plt.Figure()
        self.canvas_1 = FC(self.fig_1)
        self.fig_2 = plt.Figure()
        self.canvas_2 = FC(self.fig_2)
        self.fig_3 = plt.Figure()
        self.canvas_3 = FC(self.fig_3)
        self.fig_4 = plt.Figure()
        self.canvas_4 = FC(self.fig_4)

        self.tab1=QWidget()
        self.tab2=QWidget()
        self.tab3=QWidget()
        self.tab4=QWidget()
        self.tab5=QWidget()
        self.BSR_df = BSR_df
        self.BSR_df_index = BSR_df_index
        self.addTab(self.tab1, 'info')
        self.addTab(self.tab2, 'pool1')
        self.addTab(self.tab3, 'pool2')
        self.addTab(self.tab4, 'delta_snpindex')
        self.addTab(self.tab5, 'ed6')
        self.tab1UI()
        self.tab2UI()
        self.tab3UI()
        self.tab4UI()
        self.tab5UI()

    def tab1UI(self):
        parent_1_label = QLabel('parent_1')
        self.parent_1_combox = QComboBox()
        self.parent_1_combox.addItems(self.BSR_df_index)
        self.parent_1_combox.currentIndexChanged.connect(self.selectparent_1)

        parent_2_label = QLabel('parent_2')
        self.parent_2_combox = QComboBox()
        self.parent_2_combox.addItems(self.BSR_df_index)
        self.parent_2_index = ''
        self.parent_2_combox.setCurrentIndex(-1)
        self.parent_2_combox.currentIndexChanged.connect(self.selectparent_2)

        pool_1_label = QLabel('pool_1')
        self.pool_1_combox = QComboBox()
        self.pool_1_combox.addItems(self.BSR_df_index)
        self.pool_1_combox.currentIndexChanged.connect(self.selectpool_1)

        pool_2_label = QLabel('pool_2')
        self.pool_2_combox = QComboBox()
        self.pool_2_combox.addItems(self.BSR_df_index)
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
        min_snpindex_label = QLabel('min_snpindex')
        self.min_snpindex_spinbox = QDoubleSpinBox()
        self.min_snpindex_spinbox.setMinimum(0.0)
        self.min_snpindex_spinbox.setMaximum(0.5)
        self.min_snpindex_spinbox.setValue(0.3)
        win_size_label = QLabel('window_size')
        self.win_size_spinbox = QSpinBox()
        self.win_size_spinbox.setMinimum(100)
        self.win_size_spinbox.setMaximum(5000)
        self.win_size_spinbox.setValue(2000)
        win_step_label = QLabel('window_step')
        self.win_step_spinbox = QSpinBox()
        self.win_step_spinbox.setMinimum(0)
        self.win_step_spinbox.setMaximum(1000)
        self.win_step_spinbox.setValue(100)
        n_snp_label = QLabel('n_snp_in_window')
        self.n_snp_spinbox = QSpinBox()
        self.n_snp_spinbox.setMinimum(0)
        self.n_snp_spinbox.setMaximum(20)
        self.n_snp_spinbox.setValue(0)

        layout = QGridLayout()
        layout.addWidget(parent_1_label, 0, 0)
        layout.addWidget(self.parent_1_combox,0, 1)
        layout.addWidget(parent_2_label, 1, 0)
        layout.addWidget(self.parent_2_combox, 1, 1)
        layout.addWidget(pool_1_label, 2, 0)
        layout.addWidget(self.pool_1_combox,2, 1)
        layout.addWidget(pool_2_label, 3, 0)
        layout.addWidget(self.pool_2_combox, 3, 1)
        layout.addWidget(min_depth_label,4,0)
        layout.addWidget(self.min_depth_spinbox,4,1)
        layout.addWidget(max_depth_label,5,0)
        layout.addWidget(self.max_depth_spinbox,5,1)
        layout.addWidget(min_snpindex_label,6,0)
        layout.addWidget(self.min_snpindex_spinbox,6,1)
        layout.addWidget(next_step_button_1, 7, 1)
        layout.addWidget(win_size_label,8,0)
        layout.addWidget(self.win_size_spinbox,8,1)
        layout.addWidget(win_step_label,9,0)
        layout.addWidget(self.win_step_spinbox,9,1)
        layout.addWidget(n_snp_label,10,0)
        layout.addWidget(self.n_snp_spinbox,10,1)
        layout.addWidget(next_step_button_2,11,1)
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
        draw_layout.addWidget(self.canvas_1)

        layout = QVBoxLayout()
        layout.addLayout(draw_layout)
        layout.addLayout(tools_layout)
        self.tab2.setLayout(layout)
        down_botton_1.clicked.connect(self.download_picture_1)  
        down_botton_2.clicked.connect(self.download_window)
        down_botton_3.clicked.connect(self.download_variant)   
    
    def tab3UI(self):
        layout = QVBoxLayout()
        down_botton_4 = QPushButton('download_picture')
        down_botton_4.clicked.connect(self.download_picture_2)  
        layout.addWidget(self.canvas_2)
        layout.addWidget(down_botton_4)
        self.tab3.setLayout(layout)
    def tab4UI(self):
        layout = QVBoxLayout()
        down_botton_5 = QPushButton('download_picture')
        down_botton_5.clicked.connect(self.download_picture_3)  
        layout.addWidget(self.canvas_3)
        layout.addWidget(down_botton_5)
        self.tab4.setLayout(layout)
    def tab5UI(self):
        layout = QVBoxLayout()
        down_botton_5 = QPushButton('download_picture')
        down_botton_5.clicked.connect(self.download_picture_4)
        layout.addWidget(self.canvas_4)
        layout.addWidget(down_botton_5)
        self.tab5.setLayout(layout)

    def selectpool_1(self):
        self.pool_1_index = self.pool_1_combox.currentIndex()
    def selectpool_2(self):
        self.pool_2_index = self.pool_2_combox.currentIndex()

    def selectparent_1(self):
        self.parent_1_index = self.parent_1_combox.currentIndex()
    def selectparent_2(self):
        self.parent_2_index = self.parent_2_combox.currentIndex()  
    
    
    def clean_df(self):
        df = self.BSR_df
        min_depth = self.min_depth_spinbox.value()
        max_depth = self.max_depth_spinbox.value()
        min_snpindex =self.min_snpindex_spinbox.value()
        filed_index=[]
        filed = df.loc[0,'FORMAT'].split(':')
        filed_index.append(filed.index('GT'))
        filed_index.append(filed.index('AD'))
        filed_index.append(filed.index('DP'))
        if self.parent_2_index:
            parent_1 = df.iloc[:,self.parent_1_index].str.split(':', expand=True).iloc[:,filed_index]
            parent_1.columns = ['parent_1_gt', 'parent_1_ad','parent_1_dp']
            parent_2 = df.iloc[:,self.pool_2_index].str.split(':', expand=True).iloc[:, filed_index]
            parent_2.columns = ['parent_2_gt', 'parent_2_ad','parent_2_dp']

            pool_1 = df.iloc[:,self.pool_1_index].str.split(':', expand=True).iloc[:,filed_index]
            pool_1.columns = ['pool_1_gt', 'pool_1_ad','pool_1_dp']
            pool_2 = df.iloc[:,self.pool_2_index].str.split(':', expand=True).iloc[:, filed_index]
            pool_2.columns = ['pool_2_gt', 'pool_2_ad','pool_2_dp']
            df = pd.concat([df,parent_1,parent_2,pool_1,pool_2], axis= 1)
        #对一些需要的部分进行过滤
            df.dropna(inplace=True)
            df = df.replace(['.|.', '0|0','0|1','1|1','0|2','1|2','2|2'],['./.', '0/0','0/1','1/1','0/2','1/2','2/2'])
            df = df.replace('./.','0/0')
            df = df.replace('.', 0)
            df = df[df['parent_1_gt'].isin(['0/0','1/1'])]
            df = df[df['parent_2_gt'].isin(['0/0','1/1'])]
            df = df[df['parent_1_gt'] != df['parent_2_gt']]
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
            def get_snp_index(pool_gt,pool_ad,parent_gt = ''):
                snp_index = None
                if parent_gt:
                    if parent_gt == '0/0':
                        if pool_gt == '1/1':
                            snp_index = 1
                        elif pool_gt == '0/1':
                            snp_index = int(pool_ad.split(',')[1])/(int(pool_ad.split(',')[1])+int(pool_ad.split(',')[0]))
                        elif pool_gt == '0/0':
                            snp_index = 0
                    elif parent_gt == '1/1':
                        if pool_gt == '0/0':
                            snp_index = 1
                        elif pool_gt == '0/1':
                            snp_index = int(pool_ad.split(',')[0])/(int(pool_ad.split(',')[1])+int(pool_ad.split(',')[0]))
                        elif pool_gt == '1/1':
                            snp_index = 0
                    else:
                        snp_index = None
                else:
                    if pool_gt == '1/1':
                        snp_index = 1
                    elif pool_gt == '0/1':
                        snp_index = int(pool_ad.split(',')[1])/(int(pool_ad.split(',')[1])+int(pool_ad.split(',')[0]))
                    elif pool_gt == '0/0':
                        snp_index = 0
                    else:
                        snp_index = None
                return snp_index
            
            def get_ed6(index1,index2):
                ed6 = ((2*(index2 - index1)**2)**(0.5))**6
                return ed6
            df['pool_1_snp_index']=df.apply(lambda x: get_snp_index(x.pool_1_gt,x.pool_1_ad,x.parent_1_gt), axis = 1)
            df['pool_2_snp_index']=df.apply(lambda x: get_snp_index(x.pool_2_gt,x.pool_2_ad,x.parent_1_gt), axis = 1)
            df = df[(df['pool_1_snp_index']>min_snpindex)|(df['pool_2_snp_index']>min_snpindex)]
            df.dropna(inplace=True)
            df.eval('delta_snp_index = pool_2_snp_index-pool_1_snp_index',inplace=True)
            df['ed6'] = df.apply(lambda x:get_ed6(x.pool_1_snp_index, x.pool_2_snp_index),axis = 1)
            self.df = df[['CHROM', 'POS', 'REF', 'ALT','pool_1_gt','pool_1_snp_index','pool_2_gt','pool_2_snp_index','delta_snp_index','ed6']]
        else:
            parent_1 = df.iloc[:,self.parent_1_index].str.split(':', expand=True).iloc[:,filed_index]
            parent_1.columns = ['parent_1_gt', 'parent_1_ad','parent_1_dp']
            pool_1 = df.iloc[:,self.pool_1_index].str.split(':', expand=True).iloc[:,filed_index]
            pool_1.columns = ['pool_1_gt', 'pool_1_ad','pool_1_dp']
            pool_2 = df.iloc[:,self.pool_2_index].str.split(':', expand=True).iloc[:, filed_index]
            pool_2.columns = ['pool_2_gt', 'pool_2_ad','pool_2_dp']
            df = pd.concat([df,parent_1,pool_1,pool_2], axis= 1)
        #对一些需要的部分进行过滤
            df.dropna(inplace=True)
            df = df.replace(['.|.', '0|0','0|1','1|1','0|2','1|2','2|2'],['./.', '0/0','0/1','1/1','0/2','1/2','2/2'])
            df = df.replace('./.','0/0')
            df = df.replace('.', 0)
            df = df[df['parent_1_gt'].isin(['0/0','1/1'])]
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
            def get_snp_index(pool_gt,pool_ad,parent_gt = ''):
                snp_index = None
                if parent_gt:
                    if parent_gt == '0/0':
                        if pool_gt == '1/1':
                            snp_index = 1
                        elif pool_gt == '0/1':
                            if pool_ad.split(',')[1] != 0:
                                snp_index = int(pool_ad.split(',')[1])/(int(pool_ad.split(',')[1])+int(pool_ad.split(',')[0]))
                        elif pool_gt == '0/0':
                            snp_index = 0
                    elif parent_gt == '1/1':
                        if pool_gt == '0/0':
                            snp_index = 1
                        elif pool_gt == '0/1':
                            if pool_ad.split(',')[0] != 0:
                                snp_index = int(pool_ad.split(',')[0])/(int(pool_ad.split(',')[1])+int(pool_ad.split(',')[0]))
                        elif pool_gt == '1/1':
                            snp_index = 0
                    else:
                        snp_index = None
                else:
                    if pool_gt == '1/1':
                        snp_index = 1
                    elif pool_gt == '0/1':
                        snp_index = int(pool_ad.split(',')[1])/(int(pool_ad.split(',')[1])+int(pool_ad.split(',')[0]))
                    elif pool_gt == '0/0':
                        snp_index = 0
                    else:
                        snp_index = None
                return snp_index
            
            def get_ed6(index1,index2):
                ed6 = ((2*(index2 - index1)**2)**(0.5))**6
                return ed6

            df['pool_1_snp_index']=df.apply(lambda x: get_snp_index(x.pool_1_gt,x.pool_1_ad,x.parent_1_gt), axis = 1)
            df['pool_2_snp_index']=df.apply(lambda x: get_snp_index(x.pool_2_gt,x.pool_2_ad,x.parent_1_gt), axis = 1)
            df = df[(df['pool_1_snp_index']>min_snpindex)|(df['pool_2_snp_index']>min_snpindex)]
            df.dropna(inplace=True)
            df.eval('delta_snp_index = pool_2_snp_index-pool_1_snp_index',inplace=True)
            df['ed6'] = df.apply(lambda x:get_ed6(x.pool_1_snp_index, x.pool_2_snp_index),axis = 1)
            self.df = df[['CHROM', 'POS', 'REF', 'ALT','pool_1_gt','pool_1_snp_index','pool_2_gt','pool_2_snp_index','delta_snp_index','ed6']]

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
        def get_slide_pool_1_snp_index(chrom,window_start,window_end,df):
            n_snp = self.n_snp_spinbox.value()
            data_df = df[df['CHROM'] == chrom]
            data_df = data_df[(data_df['POS']<window_end) & (data_df['POS']> window_start)]
            if data_df.shape[0] > n_snp:
                slide_index = data_df['pool_1_snp_index'].mean()
            else:
                slide_index =None
            return slide_index
        def get_slide_pool_2_snp_index(chrom,window_start,window_end,df):
            n_snp = self.n_snp_spinbox.value()
            data_df = df[df['CHROM'] == chrom]
            data_df = data_df[(data_df['POS']<window_end) & (data_df['POS']> window_start)]
            if data_df.shape[0] > n_snp:
                slide_index = data_df['pool_2_snp_index'].mean()
            else:
                slide_index =None
            return slide_index
        def get_delta_snp_index(chrom,window_start,window_end,df):
            n_snp = self.n_snp_spinbox.value()
            data_df = df[df['CHROM'] == chrom]
            data_df = data_df[(data_df['POS']<window_end) & (data_df['POS']> window_start)]
            if data_df.shape[0] > n_snp:
                slide_index = data_df['delta_snp_index'].mean()
            else:
                slide_index =None
            return slide_index
        def get_slide_ed6(chrom,window_start,window_end,df):
            n_snp = self.n_snp_spinbox.value()
            data_df = df[df['CHROM'] == chrom]
            data_df = data_df[(data_df['POS']<window_end) & (data_df['POS']> window_start)]
            if data_df.shape[0] > n_snp:
                slide_index = data_df['ed6'].mean()
            else:
                slide_index =None
            return slide_index
        df_window['slide_pool_1_snp_index']=df_window.apply(lambda x: get_slide_pool_1_snp_index(x.chrom,x.window_start,x.window_end,self.df),axis = 1)
        df_window['slide_pool_2_snp_index']=df_window.apply(lambda x: get_slide_pool_2_snp_index(x.chrom,x.window_start,x.window_end,self.df),axis = 1)
        df_window['slide_delta_snp_index']=df_window.apply(lambda x: get_delta_snp_index(x.chrom,x.window_start,x.window_end,self.df),axis = 1)
        df_window['slide_ed6']=df_window.apply(lambda x: get_slide_ed6(x.chrom,x.window_start,x.window_end,self.df),axis = 1)
        self.df_window = df_window
    def draw(self):
        if self.chrom_count % 2 == 0:
            pic_row=self.chrom_count/2
        else:
            pic_row = (self.chrom_count+1)/2

        for i in range(0,self.chrom_count):
            draw_df_1 = self.df_window[self.df_window['chrom'] == self.chroms[i]]
            draw_df_2 = self.df[self.df['CHROM'] == self.chroms[i]]
            ax = self.fig_1.add_subplot(2,pic_row,i+1)
            ax.cla()
            ax.plot(draw_df_1['window_central']/1000000,draw_df_1['slide_pool_1_snp_index'],c='orange')
            ax.scatter(draw_df_2['POS']/1000000,draw_df_2['pool_1_snp_index'])
            ax.set_title(self.chroms[i])
            ax.set_xlabel('position (Mb)')
            ax.set_ylabel('pool_1_snp_index')
            ax.set_ylim(0, 1.01)
        self.fig_1.subplots_adjust(wspace=0.5, hspace=0.3)
        self.canvas_1.draw()
        for i in range(0,self.chrom_count):
            draw_df_1 = self.df_window[self.df_window['chrom'] == self.chroms[i]]
            draw_df_2 = self.df[self.df['CHROM'] == self.chroms[i]]
            ax = self.fig_2.add_subplot(2,pic_row,i+1)
            ax.cla()
            ax.plot(draw_df_1['window_central']/1000000,draw_df_1['slide_pool_2_snp_index'],c='orange')
            ax.scatter(draw_df_2['POS']/1000000,draw_df_2['pool_2_snp_index'])
            ax.set_title(self.chroms[i])
            ax.set_xlabel('position (Mb)')
            ax.set_ylabel('pool_2_snp_index')
            ax.set_ylim(0, 1.01)
        self.fig_2.subplots_adjust(wspace=0.5, hspace=0.3)
        self.canvas_2.draw()
        for i in range(0,self.chrom_count):
            draw_df_1 = self.df_window[self.df_window['chrom'] == self.chroms[i]]
            draw_df_2 = self.df[self.df['CHROM'] == self.chroms[i]]
            ax = self.fig_3.add_subplot(2,pic_row,i+1)
            ax.cla()
            ax.plot(draw_df_1['window_central']/1000000,draw_df_1['slide_delta_snp_index'],c='orange')
            ax.scatter(draw_df_2['POS']/1000000,draw_df_2['delta_snp_index'])
            ax.set_title(self.chroms[i])
            ax.set_xlabel('position (Mb)')
            ax.set_ylabel('delta_snp_index')
            ax.set_ylim(-1.01, 1.01)
        self.fig_3.subplots_adjust(wspace=0.5, hspace=0.3)
        self.canvas_3.draw()
        for i in range(0,self.chrom_count):
            draw_df_1 = self.df_window[self.df_window['chrom'] == self.chroms[i]]
            draw_df_2 = self.df[self.df['CHROM'] == self.chroms[i]]
            ax = self.fig_4.add_subplot(2,pic_row,i+1)
            ax.cla()
            ax.plot(draw_df_1['window_central']/1000000,draw_df_1['slide_ed6'],c='orange')
            ax.scatter(draw_df_2['POS']/1000000,draw_df_2['ed6'])
            ax.set_title(self.chroms[i])
            ax.set_xlabel('position (Mb)')
            ax.set_ylabel('ed6')
            ax.set_ylim(0, 10.1)
        self.fig_4.subplots_adjust(wspace=0.5, hspace=0.3)
        self.canvas_4.draw()

    def download_picture_1(self):
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
    def download_picture_2(self):
        filename = QFileDialog.getSaveFileName(self,'save file','','Image files(*.jpg *.gif *.png)')
        with open(filename[0],'w') as f:
            self.fig_2.savefig(filename[0],dpi=600)
    def download_picture_3(self):
        filename = QFileDialog.getSaveFileName(self,'save file','','Image files(*.jpg *.gif *.png)')
        with open(filename[0],'w') as f:
            self.fig_3.savefig(filename[0],dpi=600)
    def download_picture_4(self):
        filename = QFileDialog.getSaveFileName(self,'save file','','Image files(*.jpg *.gif *.png)')
        with open(filename[0],'w') as f:
            self.fig_4.savefig(filename[0],dpi=600)