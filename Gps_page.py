import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm
import math
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FC
from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow, QVBoxLayout, QWidget,QHBoxLayout
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *



class GpsPage(QTabWidget):
    def __init__(self,gps_df,gps_df_index):
        super(GpsPage,self).__init__()
        self.resize(800,550)
        self.setWindowTitle('Graded-pool seq')
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
        self.gps_df = gps_df
        self.gps_df_index = gps_df_index
        self.addTab(self.tab1, 'Setting')
        self.addTab(self.tab2, 'Ridit')
        self.tab1UI()
        self.tab2UI()

    def tab1UI(self):
        parent_1_label = QLabel('Parent1')
        self.parent_1_combox = QComboBox()
        self.parent_1_combox.addItems(self.gps_df_index)
        self.parent_1_combox.setCurrentIndex(-1)
        self.parent_1_index = False
        self.parent_1_combox.currentIndexChanged.connect(self.selectparent_1)

        parent_2_label = QLabel('Parent2')
        self.parent_2_combox = QComboBox()
        self.parent_2_combox.addItems(self.gps_df_index)
        self.parent_2_index = False
        self.parent_2_combox.setCurrentIndex(-1)
        self.parent_2_combox.currentIndexChanged.connect(self.selectparent_2)

        pool_1_label = QLabel('Bulk_name')
        self.pool_name_line = QLineEdit()


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
        layout.addWidget(self.pool_name_line, 2, 1)
        layout.addWidget(min_depth_label,4,0)
        layout.addWidget(self.min_depth_spinbox,4,1)
        layout.addWidget(max_depth_label,5,0)
        layout.addWidget(self.max_depth_spinbox,5,1)
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
        draw_layout.addWidget(self.canvas_1)

        layout = QVBoxLayout()
        layout.addLayout(draw_layout)
        layout.addLayout(tools_layout)
        self.tab2.setLayout(layout)
        down_botton_1.clicked.connect(self.download_picture_1)  
        down_botton_2.clicked.connect(self.download_window)
        down_botton_3.clicked.connect(self.download_variant)   


    def selectparent_1(self):
        self.parent_1_index = self.parent_1_combox.currentIndex()
    def selectparent_2(self):
        self.parent_2_index = self.parent_2_combox.currentIndex()  
    
    
    def clean_df(self):
        df = self.gps_df
        pool_names= self.pool_name_line.text().split(',')
        pool_num = len(pool_names)
        min_depth = self.min_depth_spinbox.value()
        max_depth = self.max_depth_spinbox.value()
        filed_index=[]
        filed = df.loc[0,'FORMAT'].split(':')
        filed_index.append(filed.index('GT'))
        filed_index.append(filed.index('AD'))
        filed_index.append(filed.index('DP'))
        pool_df_list = []
        for pool_name in pool_names:
            pool_df = pool_name+'_df' 
            pool_df_list.append(pool_df)
            pool_df = df[pool_name].str.split(':', expand=True).iloc[:,filed_index]
            pool_df.columns = [pool_name+'_gt', pool_name+'_ad',pool_name+'_dp']
            df = pd.concat([df,pool_df], axis= 1)
        if self.parent_1_index:
            parent_1 = df.iloc[:,self.parent_1_index].str.split(':', expand=True).iloc[:,filed_index]
            parent_1.columns = ['parent_1_gt', 'parent_1_ad','parent_1_dp']
            df = pd.concat([df,parent_1], axis= 1)
            if self.parent_2_index:
                parent_2 = df.iloc[:,self.pool_2_index].str.split(':', expand=True).iloc[:, filed_index]
                parent_2.columns = ['parent_2_gt', 'parent_2_ad','parent_2_dp']
                df = pd.concat([df,parent_2], axis= 1)
                df.dropna(inplace=True)
                df = df.replace(['.|.', '0|0','0|1','1|1','0|2','1|2','2|2'],['./.', '0/0','0/1','1/1','0/2','1/2','2/2'])
                df = df.replace('./.','0/0')
                df = df.replace('.', 0)
                df.dropna(inplace=True)
                df['parent_2_dp'] = df['parent_2_dp'].astype('str').astype('int')
                df = df[df['parent_2_dp']>min_depth]
                df = df[df['parent_2_dp']<max_depth]
                df['parent_1_dp'] = df['parent_1_dp'].astype('str').astype('int')
                df = df[df['parent_1_dp']>min_depth]
                df = df[df['parent_1_dp']<max_depth]
                df = df[df['parent_1_gt'].isin(['0/0','1/1'])]
                df = df[df['parent_2_gt'].isin(['0/0','1/1'])]
                df = df[df['parent_1_gt'] != df['parent_2_gt']]
            else:
                df = df.replace(['.|.', '0|0','0|1','1|1','0|2','1|2','2|2'],['./.', '0/0','0/1','1/1','0/2','1/2','2/2'])
                df = df.replace('./.','0/0')
                df = df.replace('.', 0)
                df.dropna(inplace=True)
                df = df[df['parent_1_gt'].isin(['0/0','1/1'])]
                df['parent_1_dp'] = df['parent_1_dp'].astype('str').astype('int')
                df = df[df['parent_1_dp']>min_depth]
                df = df[df['parent_1_dp']<max_depth]
        df = df.replace(['.|.', '0|0','0|1','1|1','0|2','1|2','2|2'],['./.', '0/0','0/1','1/1','0/2','1/2','2/2'])
        df = df.replace('./.','0/0')
        df = df.replace('.', 0)
        df.dropna(inplace=True)
        for pool_name in pool_names:
            df[pool_name+'_dp'] = df[pool_name+'_dp'].astype('str').astype('int')
            df = df[df[pool_name+'_dp']>min_depth]
            df = df[df[pool_name+'_dp']<max_depth]
            df[pool_name+'_ref'] = df[pool_name+'_ad'].str.split(',').str[0]
            df[pool_name+'_alt'] = df[pool_name+'_ad'].str.split(',').str[1]
        df.dropna(inplace=True)
        df['POS'] = df['POS'].astype('str').astype('int')   
        self.chroms = df['CHROM'].unique()
        self.chrom_count =len(self.chroms)
        df.dropna(inplace=True)
        self.chroms = df['CHROM'].unique()
        self.chrom_count =len(self.chroms)
        def get_ridit(row):
            ref = []
            alt = []
            for pool_name in pool_names:
                ref_name=pool_name+'_ref'
                alt_name=pool_name+'_alt'
                ref.append(int(row[ref_name]))
                alt.append(int(row[alt_name]))
            if sum(alt) == 0 or sum(ref) == 0:
                p = pd.NA
            else:
                m = [i + j for i, j in zip(ref, alt)]
                total = float(sum(m))
                f = list(map(lambda x: x/total ,m))
                R=[]
                for i in range(0,len(f)):
                    r=sum(f[0:i])+f[i]/2
                    R.append(r)
                ref_R = sum([i*j for i,j in zip(ref,R)])/sum(ref)
                alt_R = sum([i*j for i,j in zip(alt,R)])/sum(alt)
                SR = np.var(R, ddof = 1) 
                z=abs(ref_R-alt_R)/(SR*(1/sum(ref)+1/sum(alt))**0.5)
                p = norm.pdf(abs(z))*2
            return p
        df['p']=df.apply(lambda x: get_ridit(x), axis = 1)
        df.dropna(inplace=True)
        df['d']=df.apply(lambda x:-math.log(x.p,10),axis = 1)
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
        def get_slide_index(chrom,window_start,window_end,df):
            n_snp = self.n_snp_spinbox.value()
            data_df = df[df['CHROM'] == chrom]
            data_df = data_df[(data_df['POS']<window_end) & (data_df['POS']> window_start)]
            if data_df.shape[0] > n_snp:
                slide_index = data_df['d'].mean()
            else:
                slide_index =None
            return slide_index
        df_window['slide_d']=df_window.apply(lambda x: get_slide_index(x.chrom,x.window_start,x.window_end,self.df),axis = 1)
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
            ax.plot(draw_df_1['window_central']/1000000,draw_df_1['slide_d'],c='orange')
            ax.set_ylim(0,10.01)
            ax.axhline(y=2, c="g", ls="--")
            ax.scatter(draw_df_2['POS']/1000000,draw_df_2['d'])
            ax.set_title(self.chroms[i])
            ax.set_xlabel('position (Mb)')
            ax.set_ylabel('-log10(pvalue)')
        self.fig_1.subplots_adjust(wspace=0.5, hspace=0.3)
        self.canvas_1.draw()
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