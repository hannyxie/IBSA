# IBSA
## introduction
An Integrated GUI software for BSA-seq based on PyQt
Users can use the software to analyze and draw the VCF file. The software provides MutMap, QTL-Seq,Modified Mutmap, Grade Pool-seq,Fihser-seq.It also provides a mapping function of genome circle map. Users only need to install it to work, set parameters, and download the required pictures and tables.
## installtion
### Dependencies
- sys
- PyQt5
- pandas
- numpy
- re
- matplotlib
- scipy
- math
### download package
### down code 
## Useage
### Input file
a VCF include all sample you need,and include the variant you need.If you only focus on SNPs,use the file only include SNPs.
if you install manually,
``` python IBSA.py```
We provide these method 
|method|bulk|index|threshold|
|--|--|--|--|
Mutmap|1-2 parent,1 bulk|SNP-index|-
QTL-seq|1-2 parent,2 bulk|SNP-index,delta SNP-index,ED6|p99
Modified Mutmap|2bulk|delta SNP-index,ED6|p99
Fisher|2 bulk|-log10(p) (Fisher's exact test)|3
Graded Pool-seq|0-2 parent,>1 bulk|-log10(p) (Ridit)|the highest p window

#### 1.uplod file and choose method
<img src= "https://user-images.githubusercontent.com/51356059/116029007-f0c3e600-a68a-11eb-88ae-39cd58ddab59.png" width=400 height=320 />
#### 2.setting 
setting sample names,if you use Grade-Pool seq,please input bulk name,split by comma.firstly,click first 'NEXT' button,caculate index based on samples.
Then setting slide window paremters and click second 'NEXT' button to smooth the index.
<img src= "https://user-images.githubusercontent.com/51356059/116029818-b78c7580-a68c-11eb-8f82-badd1f328f71.png" width=400 height=320 />

4.setting
5.download file



