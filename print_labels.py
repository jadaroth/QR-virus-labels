# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 09:15:05 2024

@author: jada.roth
based on script by nicholas.lusk
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 15:37:15 2024

@author: nicholas.lusk
"""


import fpdf
import argparse
import numpy as np
import pandas as pd
import qrcode

from pathlib import Path

def create_sticker_template():
    """
    Creates the template that labels will be placed on

    Returns
    -------
    pdf : fpdf.FPDF
        fpdf object that contains the page formatting

    """
    
    pdf = fpdf.FPDF(unit = "mm", format = "letter")
    pdf.add_page()
    pdf.set_font("Helvetica", size = 8)
    pdf.set_page_background(None)
    pdf.set_auto_page_break(False) 
    
    return pdf
    
def add_sticker_cell(
        row, 
        pdf, 
        x_loc, 
        y_loc, 
        x_step = 35, 
        y_step = 25.4, 
        x_margin = 5, 
        y_margin = 13
):
    """
    This places the information from one row of the input excel file into the
    pdf output
    
    The main parameters that you will need to fine-tune are the y_step and the
    xy margin values. Note that this may mess with some of the font and you 
    can fix this by tweaking the added values in the first while statement

    Parameters
    ----------
    row : pd.Series
        a single row from the input xlsx.
    pdf : fpdf.FPDF
        An object page created from fpdf2 with the general page layout
    x_loc : int
        column value for a given label
    y_loc : int
        row value for a given sticker
    x_step : float, optional
        How long each label will be. The default is 35.
    y_step : float, optional
        how tall each label will be. The default is 25.5.
    x_margin : float, optional
        distance from the left side of the sheet that each row will be.
        The default is 3.
    y_margin : float, optional
        disctance from the top of the sheet that each column will be. 
        The default is 18.

    Returns
    -------
    None.

    """
    

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=2,
        border=1,
    )
    
    if row['Serotype'] != row['Serotype']:
        row['Serotype'] = ''
        
    if row['Name'] != row['Name']:
        row['Name'] = ' '

    qr_data = f"{row['VT']}\n{row['Plasmid']}\n{row['Name']}\n{row['Serotype']}"
    qr.add_data(qr_data)
    img = qr.make_image(back_color=(255, 255, 255), fill_color=(0, 0, 0))
        
    pdf.set_xy(2 * x_step * x_loc + x_margin, y_step * y_loc + y_margin)
    
    a, x, y = [270, 2 * x_step * x_loc + y_margin, y_step * y_loc + y_margin]
    with pdf.rotation(angle=a, x=x+11.5, y=y-7):
        pdf.set_font(style = "B")
        pdf.multi_cell(
            w = y_step,
            align=fpdf.Align.C,
            text = f"{row['VT']}",
            border=0,
            )
     
    pdf.set_xy(2 * x_step * x_loc + x_margin, y_step * y_loc + y_margin)
    with pdf.rotation(angle=a, x = x+10, y = y-8.5):
        pdf.set_font(style="")
        pdf.multi_cell(
            w = y_step,
            align=fpdf.Align.C,
            text = f"{row['Plasmid']}\n{row['Name']}\n{row['Serotype']}\n\n",
            border = 0,
        )
    
    x_offset = int(round(x_step) * 0.7)
    y_offset = int(round(y_step) * .95)
    
    pdf.image(img.get_image(), x + x_offset, y - y_offset)
            
    return

def add_data_to_template(data, save_path, x_max = 2, y_max = 10):
    """
    This loops over the data and selects what info will go into each label and
    saves as a pdf. Each sheet is saved as an individual file in the folder
    provided

    Parameters
    ----------
    data : pd.DataFrame
        dataframe with all with all the info for a given label in each row
    save_path : str
        folder where you want to save the sheets
    x_max : int
        number of columns on a sheet (zero indexed)
    y_max : int
        number of rows in a given sheet (one indexed)

    Returns
    -------
    None.

    """
    
    x_loc = 0
    y_loc = 1
    
    sheet = 1
    
    print(f"number of labels: {len(data)}")
    
    template = create_sticker_template()
    
    for c, row in data.iterrows():
        
        add_sticker_cell(row, template, x_loc, y_loc)
        
        if x_loc * y_loc == x_max * y_max:
            out_path = save_path.joinpath(f"sheet_{sheet}.pdf")
            template.output(out_path)
            template = create_sticker_template()
            sheet += 1
            x_loc = 0
            y_loc = 1
        elif y_loc == y_max:
            x_loc += 1
            y_loc = 1
        else:
            y_loc += 1
            
    print(x_loc)
    print(y_loc)
            
    if x_loc == 0 and y_loc == 1:
        return
    else:
        out_path = save_path.joinpath(f"sheet_{sheet}.pdf")
        template.output(out_path)
        return

def main(filepath, save_path):
    """
    Main function that creates and saves the label sheet

    Parameters
    ----------
    filepath : str
        the excel file that you want to create labels from
    save_path : str
        the location where you want to save the label sheets

    Returns
    -------
    None.

    """
    
    df = pd.read_csv(Path(filepath))
    add_data_to_template(df, Path(save_path), 2, 10)
    
    
    return 

if __name__ == "__main__":
    """
    This will be executed when the script is run in terminal. The two inputs 
    needed are the xlsx file with the data and the path where you want to save 
    the outputs
    
    
    Example: python -m label_template_creator /Users/nicholas.lusk/Desktop/tic_tac_QR_code.csv /Users/nicholas.lusk/Desktop

    """
    
    parser = argparse.ArgumentParser()
    parser.add_argument("filepath", type = str, help = "Insert full pathway to excel xlsx file you want to process")
    parser.add_argument("save_path", type = str, help = "Insert the full pathway to where you want to save the files")
    
    args = parser.parse_args()
    
    main(args.filepath, args.save_path)

