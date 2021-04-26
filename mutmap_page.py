import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FC
from scipy.stats import mannwhitneyu
from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow, QVBoxLayout, QWidget,QHBoxLayout
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *



class MutmapPage(QTabWidget):
    def __init__(self,mutmap_df,mutmap_df_index):
        super(MutmapPage,self).__init__()
        self.resize(800,550)
        self.setWindowTitle('Mutmap')
        self.fig = plt.Figure()
        self.canvas = FC(self.fig)
        self.tab1=QWidget()
        self.tab2=QWidget()
        self.mutmap_df = mutmap_df
        self.mutmap_df_index = mutmap_df_index
        self.addTab(self.tab1, 'Setting')
        self.addTab(self.tab2, 'SNP-index')
        self.tab1UI()
        self.tab2UI()


    def tab1UI(self):
        parent_1_label = QLabel('Parent1')
        self.parent_1_combox = QComboBox()
        self.parent_1_combox.addItems(self.mutmap_df_index)
        self.parent_1_combox.currentIndexChanged.connect(self.selectparent_1)

        parent_2_label = QLabel('Parent2')
        self.parent_2_combox = QComboBox()
        self.parent_2_combox.addItems(self.mutmap_df_index)
        self.parent_2_index = ''
        self.parent_2_combox.setCurrentIndex(-1)
        self.parent_2_combox.currentIndexChanged.connect(self.selectparent_2)

        pool_1_label = QLabel('Bulk')
        self.pool_1_combox = QComboBox()
        self.pool_1_combox.addItems(self.mutmap_df_index)
        self.pool_1_combox.currentIndexChanged.connect(self.selectpool_1)



        next_step_button_1 = QPushButton('Next')
        next_step_button_1.clicked.connect(self.clean_df)
        next_step_button_2 = QPushButton('Next')
        next_step_button_2.clicked.connect(self.slide_window)

        min_depth_label = QLabel('Min_depth')
        self.min_depth_spinbox = QSpinBox()
        self.min_depth_spinbox.setMinimum(0)
        self.min_depth_spinbox.setMaximum(15)
        self.min_depth_spinbox.setValue(5)
        max_depth_label = QLabel('Max_depth')
        self.max_depth_spinbox = QSpinBox()
        self.max_depth_spinbox.setMinimum(200)
        self.max_depth_spinbox.setMaximum(500)
        self.max_depth_spinbox.setValue(300)
        min_snpindex_label = QLabel('Min_snpindex')
        self.min_snpindex_spinbox = QDoubleSpinBox()
        self.min_snpindex_spinbox.setMinimum(0.0)
        self.min_snpindex_spinbox.setMaximum(0.5)
        self.min_snpindex_spinbox.setValue(0.3)
        win_size_label = QLabel('Window_size')
        self.win_size_spinbox = QSpinBox()
        self.win_size_spinbox.setMinimum(100)
        self.win_size_spinbox.setMaximum(5000)
        self.win_size_spinbox.setValue(2000)
        win_step_label = QLabel('Window_step')
        self.win_step_spinbox = QSpinBox()
        self.win_step_spinbox.setMinimum(0)
        self.win_step_spinbox.setMaximum(1000)
        self.win_step_spinbox.setValue(100)
        n_snp_label = QLabel('N_snp_in_window')
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

        btn_start = QPushButton('Plot')
        btn_start.clicked.connect(self.draw)
        down_botton_1 = QPushButton('Download_picture')
        down_botton_2 = QPushButton('Download_window')
        down_botton_3 = QPushButton('Download_variant')
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

    def selectpool_1(self):
        self.pool_index = self.pool_1_combox.currentIndex()


    def selectparent_1(self):
        self.parent_1_index = self.parent_1_combox.currentIndex()
    def selectparent_2(self):
        self.parent_2_index = self.parent_2_combox.currentIndex() 
    
    def clean_df(self):
        df = self.mutmap_df
        min_depth = self.min_depth_spinbox.value()
        max_depth = self.max_depth_spinbox.value()
        min_snpindex =self.min_snpindex_spinbox.value()
        filed_index=[]
        filed = df.loc[0,'FORMAT'].split(':')
        filed_index.append(filed.index('GT'))
        filed_index.append(filed.index('AD'))
        filed_index.append(filed.index('DP'))
        parent1 = df.iloc[:,self.parent_1_index].str.split(':', expand=True).iloc[:,filed_index]
        parent1.columns = ['parent1_gt', 'parent1_ad','parent1_dp']
        pool = df.iloc[:,self.pool_index].str.split(':', expand=True).iloc[:, filed_index]
        pool.columns = ['pool_gt', 'pool_ad','pool_dp']
        df = pd.concat([df,parent1,pool], axis= 1)
        #对一些需要的部分进行过滤
        df.dropna(inplace=True)
        df = df.replace(['.|.', '0|0','0|1','1|1','0|2','1|2','2|2','.'],['./.', '0/0','0/1','1/1','0/2','1/2','2/2','0'])
        df = df[df['parent1_gt'].isin(['0/0','1/1'])]
        print(self.parent_2_index)
        if self.parent_2_index:
            parent2 = df.iloc[:,self.parent_2_index].str.split(':', expand=True).iloc[:,filed_index]
            parent2.columns = ['parent2_gt', 'parent2_ad','parent2_dp']
            df = pd.concat([df,parent2], axis= 1)
            df = df[df['parent2_gt'].isin(['0/0','1/1'])]
            df = df[df['parent1_gt'] != df['parent2_gt']]
            df['parent2_dp'] = df['parent2_dp'].astype('str').astype('int')
            df = df[df['parent2_dp']>min_depth]
            df = df[df['parent2_dp']<max_depth]
        df['parent1_dp'] = df['parent1_dp'].astype('str').astype('int')
        df['pool_dp'] = df['pool_dp'].astype('str').astype('int')
        df['POS'] = df['POS'].astype('str').astype('int')
        df = df[df['parent1_dp']>min_depth]
        df = df[df['parent1_dp']<max_depth]
        df = df[df['pool_dp']>min_depth]
        df = df[df['pool_dp']<max_depth]
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
                        if (int(pool_ad.split(',')[1])+int(pool_ad.split(',')[0])) != 0:
                            snp_index = int(pool_ad.split(',')[1])/(int(pool_ad.split(',')[1])+int(pool_ad.split(',')[0]))
                    elif pool_gt == '0/0':
                        snp_index = 0
                elif parent_gt == '1/1':
                    if pool_gt == '0/0':
                        snp_index = 1
                    elif pool_gt == '0/1':
                        if (int(pool_ad.split(',')[1])+int(pool_ad.split(',')[0])) != 0:
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
            
        df['snp_index']=df.apply(lambda x: get_snp_index(x.pool_gt,x.pool_ad,x.parent1_gt), axis = 1)
        df = df[(df['snp_index']>min_snpindex)]
        df.dropna(inplace=True)
        self.df = df

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
        def get_slide_index(chrom,window_start,window_end):
            n_snp = self.n_snp_spinbox.value()
            data_df = df[df['CHROM'] == chrom]
            data_df = data_df[(data_df['POS']<window_end) & (data_df['POS']> window_start)]
            if data_df.shape[0] > n_snp:
                slide_index = data_df['snp_index'].mean()
            else:
                slide_index =None
            return slide_index
        df_window['slide_snp_index'] = df_window.apply(lambda x: get_slide_index(x.chrom,x.window_start,x.window_end),axis = 1)
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
            ax.plot(draw_df_1['window_central']/1000000,draw_df_1['slide_snp_index'],c='red')
            ax.scatter(draw_df_2['POS']/1000000,draw_df_2['snp_index'],color='blue')
            ax.axhline(y=0.9, c="g", ls="--")
            ax.set_title(self.chroms[i])
            ax.set_xlabel('position (Mb)')
            ax.set_ylabel('SNP-index')
            ax.set_ylim(0, 1.05)
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
