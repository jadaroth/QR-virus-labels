# QR-virus-labels: Description

This script will generate labels with QR codes for the tic-tac boxes used by the Viral Technology Core and saves the file as a pdf in your output directory. The labels used are from International LabTag, catalog number: LCS-3WH. These sheets have 30 stickers per label. If you generate more than 30 labels at a time, separate pdfs will be saved to your computer. 

The "print_labels.py" script reads in a csv file that contains the following header names:

VT, Plasmid, Name, Serotype, and FullName. 

Plain text will be printed on the label, showing VT, Plasmid, Name, and Serotype (if not PHP.eB). 

A QR code is also generated, encoding the VT # only. The Plasmid's FullName is printed in plain text above the QR code.


**Generate a conda environment with following:**

python version 3.9, fpdf2, qrcode, pandas, and anaconda::spyder

**The conda environment only needs to be created once. Afterwards, you can simply re-activate it**
```
## In your terminal/console, type the following line-by-line and follow prompts
conda create -n "NAME" python = 3.9
```
```
conda activate "NAME"
```
```
cd /Users/jada.roth/Desktop
## Use the path where your input files are located. Here, my files are located on my Desktop
```
```
pip install fpdf2 qrcode
```
```
conda install pandas
```
```
conda install anaconda::spyder
```

**Running script**
```
conda activate "NAME"
```
```
## Change directory to the path where your input csv and module are located
cd /Users/jada.roth/Desktop
```
```
python -m NAME Path1 Path2
## Path 1 is where your input CSV is located
## Path 2 is where you'd like to output your label pdf
```

**Printing labels**

Make sure to print using "actual size" in your scale options. Otherwise, alignment will be off. 

**Change log**
04/18/2025: 
Updated README with more robust instructions and descriptions. 
12/23/2024: Updated print_labels.py, uploaded tic_tac_QR_code.csv as example input file, uploaded tutorial word document. 
